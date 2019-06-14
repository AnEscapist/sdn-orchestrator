from __future__ import print_function
import libvirt
import sys

conn=libvirt.open("qemu+tcp://potato@10.10.81.5/system")
print(conn)

domainIDs = conn.listDomainsID()
if domainIDs == None:
    print('Failed to get a list of odmain IDs', file=sys.stderr)

print("Active domain IDs:")
if len(domainIDs) == 0:
    print(' None')
else:
    for domainID in domainIDs:
        print(' '+str(domainID))

conn.close()
exit(0)
