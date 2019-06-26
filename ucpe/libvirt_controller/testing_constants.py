from ucpe.ucpe import UCPE
from ucpe.libvirt_controller.utils import read

DEFAULT_UCPE = UCPE(username="potato", hostname="10.10.81.100")
DEFAULT_XML_PATH = "/home/attadmin/projects/sdn-orchestrator/ucpe/agent-vm/ubuntu_test.xml"
DEFAULT_XML = read("/home/attadmin/projects/sdn-orchestrator/ucpe/agent-vm/ubuntu_networking_cloud-init.xml")
# DEFAULT_KWARGS = {"body":{"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "xml": DEFAULT_XML, "autostart": 1, "save_path": "/home/potato/save_path.test"}}
DEFAULT_KWARGS = {"body":{"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1, "save_path": "/home/potato/save_path.test"}}





def read1(path):
    file = None
    try:
        file = open(path)
        return file.read()
    finally:
        file.close()

def read2(path):
    with open(path) as file:
        return file.read()

