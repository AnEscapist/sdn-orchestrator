from __future__ import print_function
import libvirt
from libvirt import *
from enum import Enum
import sys

conn=libvirt.open("qemu+tcp://potato@10.10.81.100/system")
print(conn)

domainIDs = conn.listAllDomains()
print(domainIDs)
conn.close()

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



