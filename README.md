# Network Programmability Basics

Code, Examples, and Resources for the Network Programmability Basics Video Course

## Automatic source checks and live tutorial exercises

Automatic CI retains Python **3.8.20** and all seven original workflow
producers: Part 1 arithmetic, Part 2 shapes and time, and Part 3 NETCONF,
CLI, SNMP, RESTCONF and data-format examples. The authored examples, their
original requirements and data files remain unchanged.

**Automatic external network execution is replaced by offline source-contract
checks. These checks do not qualify a live network, device, sandbox or VPN.**
The original examples still describe manual tutorial exercises. Their historical
sandbox addresses, credentials, TLS settings and library APIs require a separate
environment review before live use. CI does not establish that those settings
remain valid or safe for a current network.

The offline profile imports compatible real dependencies and executes the
original scripts. Narrow fixtures replace NETCONF connection, CLI connection,
REST GET and SNMP GET entry functions. The real SNMP numeric-address resolver
uses a fixture that validates an IPv4 address and port 161 without DNS. A separate
socket guard rejects DNS and TCP/UDP sends, including negative tests that prove
accidental network access fails. Assertions check request shape, parsed results,
the SNMP success and both error branches, deterministic arithmetic, timestamp
arithmetic, and the original XML, JSON, YAML and CSV exercises. No unrelated
device configuration or application-hosting example runs automatically.

Each of the seven producers has an explicit CI step and JUnit receipt. The job
also records the actual interpreter, installed dependencies and all tracked file
digests before and after execution. Any failed producer fails the single complete
job. Later producers and evidence collection still run after a failure. Only
obsolete runs within one pull request can cancel each other; branch runs remain
independent. The workflow admits only push and pull-request events
for `master`, has read-only repository permission, and publishes test artifacts.
It contains no deployment, release or package publisher.

For an isolated local check with an existing Python 3.8.20 interpreter:

```sh
python3.8 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-ci.txt
.venv/bin/python -m ruff check tests
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -v tests
```

The CI-only hash-locked dependencies preserve the tutorial APIs on Python 3.8.
They do not replace the original lesson requirements or claim production
dependency support. Regenerate the lock in an owned Python 3.8.20 environment
with `uv pip compile --python .venv/bin/python --no-header --generate-hashes
--output-file requirements-ci.txt requirements-ci.in`, then rerun all checks.

## Table of Contents
* [General Workstation Setup](readme_resources/workstation_setup.md)
    * [Operating System Considerations](readme_resources/workstation_setup.md#operating-system-considerations)
    * [Setting up git](readme_resources/workstation_setup.md#setting-up-git)
    * [Setting Up Python](readme_resources/workstation_setup.md#setting-up-python)
    * [Postman](readme_resources/workstation_setup.md#postman)
    * [DevNet Sandbox VPN Access](readme_resources/workstation_setup.md#devnet-sandbox-vpn-access)
* [Programming Fundamentals](programming_fundamentals/README.md)
    * [Data Formats: Understanding and using JSON, XML and YAML](programming_fundamentals/data_formats/README.md)
    * [APIs are Everywhere... but what are they?](programming_fundamentals/apis/README.md)
    * [REST APIs Part 1: HTTP is for more than Web Browsing](programming_fundamentals/rest_part_1/README.md)
    * [REST APIs Part 2: Making REST API Calls with Postman](programming_fundamentals/rest_part_2/README.md)
    * [Python Part 1: Python Language and Script Basics](programming_fundamentals/python_part_1/README.md)
    * [Python Part 2: Working with Libraries and Virtual Environments](programming_fundamentals/python_part_2/README.md)
    * [Python Part 3: Useful Python Libraries for Network Engineers](programming_fundamentals/python_part_3/README.md)
* [Network Device APIs](network_device_apis/README.md)
    * [Getting the “YANG” of it with Standard Data Models](network_device_apis/yang/README.md)
    * [Goodbye SNMP <hello> NETCONF!](network_device_apis/netconf/README.md)
    * [Learn to CRUD with GET, POST and DELETE using RESTCONF](network_device_apis/restconf/README.md)
    * [NX-API Part 1: Get Started with APIs and Nexus](network_device_apis/nxapi/README.md)
    * [NX-API Part 2: Dive into the Nexus Object Model](network_device_apis/nxapi/README.md)
* [Network Controllers](network_controllers/README.md)
    * [Program your own DNA with APIC-EM APIs](network_controllers/apicem/README.md)
    * [Got SDN? Understanding the ACI Programmability Options](network_controllers/aci/README.md)
    * [Network Control in the Cloud - Developing with Cisco Meraki](network_controllers/meraki/README.md)
    * [DNA APIs Part 1: Exploring APIC-EM Apps via API](network_controllers/apicem/README.md)
    * [DNA APIs Part 2: Troubleshooting with APIC-EM Programmability](network_controllers/apicem/README.md)
    * [ACI Programmability Part 1: The ACI Object Model](network_controllers/aci/README.md)
    * [ACI Programmability Part 2: Using the ACI Toolkit](network_controllers/aci/README.md)
* [Application Hosting and the Network](application_hosting/README.md)
    * [Cloud to Fog… Why Host Apps in the Network](application_hosting/intro/README.md)
    * [Linux at the Edge: Introduction to Guest Shell](application_hosting/guestshell/README.md)
    * [Python at the Edge: Super Charged Network Event Management](application_hosting/python_onbox/README.md)
    * [Package, Deploy and Run Applications in the Network with IOx](application_hosting/iox/README.md)
* [NetDevOps](netdevops/README.md)
    * [Configuration Management and the Network](netdevops/intro/README.md)
    * [Ansible Part 1: What you need to Get Started](netdevops/ansible_part_1/README.md)
    * [Ansible Part 2: Using Ansible for Network Configuration](netdevops/ansible_part_2/README.md)
    * [Ansible Part 3: Your Network As Code](netdevops/ansible_part_3/README.md)
