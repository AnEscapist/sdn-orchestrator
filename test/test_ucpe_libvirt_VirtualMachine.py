from ucpe.libvirt.VirtualMachine import *
from ucpe.libvirt.testing_constants import *
import time
import pytest


# @pytest.mark.tryfirst
# def test_virtual_machine_integrated():
#     # test defaults
#     # todo: figure out what to do with the sleeps
#     vm = VirtualMachine.define(DEFAULT_UCPE, DEFAULT_XML_PATH)
#     assert vm.state == VMState.SHUTOFF
#     vm.start()
#     xml_excerpt = "<domain type='kvm' id='34'>"
#     assert vm.xml.find(xml_excerpt)
#     assert vm.state == VMState.RUNNING
#     vm.suspend()
#     time.sleep(5)
#     assert vm.state == VMState.PAUSED
#     vm.resume()
#     time.sleep(20)
#     assert vm.state == VMState.RUNNING
#     vm.shutdown()
#     time.sleep(20)
#     assert vm.state == VMState.SHUTOFF
#     vm.undefine()
#     time.sleep(10)
#     with pytest.raises(libvirt.libvirtError) as error_info:
#         vm.state #shouldn't be able to get state of undefined vm

@pytest.mark.trylast
def test_demonstrate_shutdown_bug():
    #test defaults
    vm = VirtualMachine.define(DEFAULT_UCPE, DEFAULT_XML_PATH)
    vm.start()
    vm.shutdown()
