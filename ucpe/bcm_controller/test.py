from ucpe.bcm_controller.bcm_controller import *

destroy_vlan("135.91.120.243:50051", 100)
print(show_vlans("135.91.120.243:50051"))
