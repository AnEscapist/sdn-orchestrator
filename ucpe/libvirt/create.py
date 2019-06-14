import libvirt
import sys

def read_file(path):
    contents = []
    with open(path) as f:
        for line in f:
            contents.append(line)
    return "".join(contents)

xml = read_file("fortigate3.xml")
conn=libvirt.open("qemu+tcp://potato@10.10.81.5/system")
dom = conn.createXML(xml, 0)
if dom == None:
    print("you failed")
    exit(1)

print('Guest ' + dom.name() + ' has booted', file=sys.stderr)

conn.close()
exit(0)
