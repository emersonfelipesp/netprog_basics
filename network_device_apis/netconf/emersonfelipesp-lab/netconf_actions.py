from click import pass_obj
from ncclient import manager
import xmltodict

from device_info import ios_xe

class Netconf:
    def __init__():
        with manager.connect(
            host=ios_xe["address"],
            port=ios_xe["port"],
            username=ios_xe["username"],
            password=ios_xe["passowrd"],
            hostkey_verify=False
        ) as m:

    def get():
        print(self.m)
        teste
    
    def get_config():
        pass

    def edit_config():
        pass
