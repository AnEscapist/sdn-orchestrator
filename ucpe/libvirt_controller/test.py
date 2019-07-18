# from __future__ import print_function
from web.backend.zmq_web import start, call_ucpe_function
from time import sleep
import libvirt
from libvirt import *
from enum import Enum
import sys

# conn = libvirt.open("qemu+tcp://potato@10.10.81.100/system")
# print(conn)
#
# domainIDs = conn.listAllDomains()
# print(domainIDs)
# conn.close()

# class Color(Enum):
#     RED = 1
#     BLUE = 2
#     GREEN = 3
#
# red = Color.RED
# print(red)

# print(VIR_DOMAIN_NOSTATE)
# print(VIR_DOMAIN_RUNNING)
# print(VIR_DOMAIN_BLOCKED)
# print(VIR_DOMAIN_PAUSED)
# print(VIR_DOMAIN_SHUTDOWN)
# print(VIR_DOMAIN_SHUTOFF)
# print(VIR_DOMAIN_CRASHED)
# print(VIR_DOMAIN_PMSUSPENDED)

start()
sleep(2)
messagedata = {"method": "libvirt_controller_get_all_vm_info", "params": {
    "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
             "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

result = call_ucpe_function(messagedata)
print(result)
