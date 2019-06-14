from __future__ import print_function
import libvirt
import sys

conn=libvirt.open("qemu+tcp://potato@10.10.81.5/system")
print(conn)
domains = conn.listAllDomains()
domain_to_stop = "fortigate3"
for domain in domains:
    if domain.name() == domain_to_stop:
        domain.shutdown()

conn.close()
exit(0)
