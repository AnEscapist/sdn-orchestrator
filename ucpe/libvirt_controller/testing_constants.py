from ucpe.UCPE import UCPE
from ucpe.libvirt_controller.utils import read

DEFAULT_UCPE = UCPE(username="potato", hostname="10.10.81.100")
DEFAULT_XML_PATH = "/home/attadmin/projects/sdn-orchestrator/ucpe/agent-vm/ubuntu_test.xml"
DEFAULT_XML = read("/home/attadmin/projects/sdn-orchestrator/ucpe/agent-vm/ubuntu_test.xml")
DEFAULT_KWARGS = {"body":{"username": "potato", "hostname": "10.10.81.100", "vm_name": "test"}}
