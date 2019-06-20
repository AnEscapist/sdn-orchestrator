from ucpe.UCPE import UCPE
import ucpe.libvirt_controller.utils as virtutils
from ucpe.libvirt_controller.testing_constants import *
from ucpe.libvirt_controller.VirtualMachine import *

#todo: figure out how to make a new class for each function

# def test_connect():
#     #test defaults
#     conn_default = virtutils.connect()
#     conn_default.close()
#     #test ucpe
#     ucpe = DEFAULT_UCPE
#     conn_ucpe = virtutils.connect(ucpe=ucpe)
#     conn_ucpe.close()
#
def test_all_domain_states():
    ucpe = DEFAULT_UCPE
    vm = VirtualMachine.define(DEFAULT_UCPE, DEFAULT_XML_PATH)
    states = virtutils.all_vm_states(ucpe)
    assert states['test'] == VMState.SHUTOFF
    #todo: tests are bad
    vm.undefine()
#
# def test_read():
#     #TODO: replace with relative path
#     virtutils.read("/home/attadmin/projects/sdn-orchestrator/ucpe/agent-vm/ubuntu.xml")
