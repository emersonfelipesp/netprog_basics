"""Execute the seven unchanged producers with explicit offline network contracts."""

from __future__ import annotations

import ast
import datetime
import hashlib
import ipaddress
import json
import runpy
import socket
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Iterator
from unittest.mock import Mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
FUNDAMENTALS = ROOT / "programming_fundamentals"
PART3 = FUNDAMENTALS / "python_part_3"
PRODUCERS = (
    "python_part_1/example1.py",
    "python_part_2/example1.py",
    "python_part_3/api_ncclient_example.py",
    "python_part_3/api_netmiko_example.py",
    "python_part_3/api_pysnmp_example.py",
    "python_part_3/api_requests_example.py",
    "python_part_3/data_library_exercises.py",
)


def reject_network(*args, **kwargs) -> None:
    raise AssertionError("Offline source contracts prohibit network access")


@pytest.fixture(autouse=True)
def offline_and_immutable(monkeypatch) -> Iterator[None]:
    paths = sorted(FUNDAMENTALS.glob("python_part_[123]/*"))
    before = {
        p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()
    }
    monkeypatch.setattr(socket, "create_connection", reject_network)
    monkeypatch.setattr(socket, "getaddrinfo", reject_network)
    for method in ("connect", "connect_ex", "sendto", "send", "sendall"):
        monkeypatch.setattr(socket.socket, method, reject_network)
    yield
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in before}
    assert before == after


def run_example(relative, monkeypatch, arguments=()) -> dict:
    target = FUNDAMENTALS / relative
    monkeypatch.chdir(target.parent)
    monkeypatch.syspath_prepend(str(target.parent))
    monkeypatch.setattr(sys, "argv", [str(target), *arguments])
    return runpy.run_path(str(target), run_name="__main__")


def test_required_python38_and_complete_producer_selection() -> None:
    assert sys.version_info[:3] == (3, 8, 20)
    assert len(PRODUCERS) == 7
    for producer in PRODUCERS:
        ast.parse((FUNDAMENTALS / producer).read_text())


@pytest.mark.parametrize("operation", ["dns", "tcp", "udp"])
def test_network_guard_fails_closed(operation) -> None:
    with pytest.raises(AssertionError, match="prohibit network"):
        if operation == "dns":
            socket.getaddrinfo("example.invalid", 443)
        elif operation == "tcp":
            with socket.socket() as connection:
                connection.connect(("127.0.0.1", 443))
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
                connection.sendto(b"forbidden", ("127.0.0.1", 161))


@pytest.mark.parametrize(
    "number,expected", [("5", "10.0"), ("-2.5", "-5.0"), ("0", "0.0")]
)
def test_part1_arithmetic_producer(number, expected, monkeypatch, capsys) -> None:
    run_example(PRODUCERS[0], monkeypatch, [number])
    assert capsys.readouterr().out.strip() == expected


@pytest.mark.parametrize("arguments", [(), ("not-a-number",)])
def test_part1_invalid_input(arguments, monkeypatch, capsys) -> None:
    with pytest.raises(SystemExit) as error:
        run_example(PRODUCERS[0], monkeypatch, arguments)
    assert error.value.code == 1
    assert "You must provide a number" in capsys.readouterr().out


def test_part2_shapes_and_timestamp_producer(monkeypatch, capsys) -> None:
    result = run_example(PRODUCERS[1], monkeypatch)
    output = capsys.readouterr().out
    for shape in result["shapes"]:
        assert shape in output
    assert result["new_date"] - result["date_now"] == datetime.timedelta(minutes=1000)
    assert str(result["date_now"]) in output
    assert str(result["new_date"]) in output


def test_part3_ncclient_producer(monkeypatch, capsys) -> None:
    from ncclient import manager

    xml = """<rpc-reply><data><interfaces><interface><name xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">GigabitEthernet1</name></interface></interfaces></data></rpc-reply>"""
    connection = Mock()
    connection.get_config.return_value = SimpleNamespace(xml=xml)
    connect = Mock(return_value=connection)
    monkeypatch.setattr(manager, "connect", connect)
    result = run_example(PRODUCERS[2], monkeypatch)
    router = result["router"]
    connect.assert_called_once_with(
        host=router["ip"],
        port=router["port"],
        username=router["user"],
        password=router["pass"],
        hostkey_verify=False,
    )
    connection.get_config.assert_called_once_with("running", result["netconf_filter"])
    assert "GigabitEthernet1" in result["netconf_filter"]
    assert capsys.readouterr().out.strip() == repr("GigabitEthernet1")


def test_part3_netmiko_producer(monkeypatch, capsys) -> None:
    import netmiko

    connection = Mock()
    connection.send_command.return_value = (
        "interface GigabitEthernet1\n description offline fixture"
    )
    connect = Mock(return_value=connection)
    monkeypatch.setattr(netmiko, "ConnectHandler", connect)
    result = run_example(PRODUCERS[3], monkeypatch)
    router = result["router"]
    connect.assert_called_once_with(
        ip=router["host"],
        port=router["port"],
        username=router["user"],
        password=router["pass"],
        device_type=router["device_type"],
    )
    connection.send_command.assert_called_once_with("show run int Gig1")
    assert result["interface_cli"] == connection.send_command.return_value
    assert "offline fixture" in capsys.readouterr().out


def test_part3_requests_producer(monkeypatch, capsys) -> None:
    import requests

    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(
        {"Cisco-IOS-XE-interfaces-oper:interface": {"name": "GigabitEthernet1"}}
    ).encode()
    get = Mock(return_value=response)
    monkeypatch.setattr(requests, "get", get)
    result = run_example(PRODUCERS[5], monkeypatch)
    router = result["router"]
    get.assert_called_once_with(
        "https://{}:{}/restconf/data/interfaces/interface=GigabitEthernet1".format(
            router["ip"], router["port"]
        ),
        headers={"Accept": "application/yang-data+json"},
        auth=(router["user"], router["pass"]),
        verify=False,
    )
    assert result["interface_name"] == "GigabitEthernet1"
    assert "GigabitEthernet1" in capsys.readouterr().out


@pytest.mark.parametrize(
    "mode,index",
    [("success", 0), ("engine-error", 0), ("agent-error", 1), ("agent-error", 0)],
)
def test_part3_pysnmp_producer(mode, index, monkeypatch, capsys) -> None:
    from pysnmp import hlapi

    monkeypatch.setattr(
        hlapi.UdpTransportTarget, "_resolveAddr", offline_numeric_address
    )
    error = Mock()
    error.prettyPrint.return_value = "fixture agent error"
    bindings = [
        (
            SimpleNamespace(prettyPrint=lambda: "sysDescr.0"),
            SimpleNamespace(prettyPrint=lambda: "offline router"),
        )
    ]
    response = {
        "success": (None, 0, 0, bindings),
        "engine-error": ("fixture engine error", 0, 0, []),
        "agent-error": (None, error, index, ["sysDescr.0"]),
    }[mode]
    get = Mock(return_value=iter([response]))
    monkeypatch.setattr(hlapi, "getCmd", get)
    result = run_example(PRODUCERS[4], monkeypatch)
    assert_snmp_request(get, result["router"])
    assert_snmp_oid_source()
    assert_snmp_output(mode, index, capsys.readouterr().out)


def offline_numeric_address(self, address) -> tuple:
    ipaddress.IPv4Address(address[0])
    assert address[1] == 161
    return address


def test_part3_data_library_producer(monkeypatch, capsys) -> None:
    result = run_example(PRODUCERS[6], monkeypatch)
    assert result["xml_dict"]["interface"]["name"] == "GigabitEthernet2"
    assert (
        result["json_python"]["ietf-interfaces:interface"]["name"] == "GigabitEthernet2"
    )
    assert (
        result["yaml_python"]["ietf-interfaces:interface"]["name"] == "GigabitEthernet2"
    )
    output = capsys.readouterr().out
    assert "Import Spreadsheets and Data with csv" in output
    assert "has IP" in output


def assert_snmp_request(get, router) -> None:
    from pysnmp import hlapi

    args = get.call_args.args
    assert get.call_count == 1
    assert isinstance(args[0], hlapi.SnmpEngine)
    assert args[1].communityName == "public"
    assert args[2].transportAddr == (router["ip"], router["port"])
    assert isinstance(args[3], hlapi.ContextData)
    assert isinstance(args[4], hlapi.ObjectType)


def assert_snmp_oid_source() -> None:
    tree = ast.parse((PART3 / "api_pysnmp_example.py").read_text())
    identity = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "ObjectIdentity"
    ]
    assert len(identity) == 1
    assert [arg.value for arg in identity[0].args] == ["SNMPv2-MIB", "sysDescr", 0]


def assert_snmp_output(mode, index, output) -> None:
    expected = {
        "success": "sysDescr.0 = offline router",
        "engine-error": "fixture engine error",
        "agent-error": "fixture agent error",
    }[mode]
    assert expected in output
    if mode == "engine-error":
        assert "connected to the VPN" in output
    if mode == "agent-error":
        assert ("sysDescr.0" if index else "?") in output
