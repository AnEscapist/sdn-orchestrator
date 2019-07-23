from ucpe.bcm_controller.bcm_controller import *
from web.backend.zmq_web import call_ucpe_function, start
import time


# create_vlan("135.91.120.243:50051", 100)
# add_ports("135.91.120.243:50051", 100, "ge4,ge9")
# add_ports("135.91.120.243:50051", 100, "ge4,ge9,xe4")
# rem_ports("135.91.120.243:50051", 100, "ge4,ge9,xe4")
# add_ports("135.91.120.243:50051", 100, "ge4,ge9,xe4", "ge4")
# destroy_vlan("135.91.120.243:50051", 100)
#
# print(show_vlans("135.91.120.243:50051"))
# set_pvlan("135.91.120.243:50051", 100, "ge4")
# print(show_pvlans("135.91.120.243:50051"))

DEFAULT_KWARGS = {"body": {"vlanid": 100, "hostname": "135.91.120.243:50051", "pbm": "ge4,ge9,xe9", "ubm": "ge9", "vm_name": "test", "autostart": 1, "save_path": "/home/potato/save_path.test", "image_path": "/var/third-party/ubuntu_16_roger.qcow2"}}
# BCMController.bcm_controller_destroy_vlan(**DEFAULT_KWARGS)
# return_dict = BCMController.bcm_controller_show_pvlans(**DEFAULT_KWARGS)
# print(return_dict["result"])

messagedata = {"method": "bcm_controller_create_vlan",
    "params": {"body": DEFAULT_KWARGS}, "jsonrpc": "2.0",
    "id": 0}
start()
time.sleep(2)

print(call_ucpe_function(messagedata))
