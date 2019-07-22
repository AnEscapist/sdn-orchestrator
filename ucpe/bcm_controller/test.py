from ucpe.bcm_controller.bcm_controller import *

create_vlan("135.91.120.243:50051", 100)
add_ports("135.91.120.243:50051", 100, "ge4,ge9")
add_ports("135.91.120.243:50051", 100, "ge4,ge9,xe4")
rem_ports("135.91.120.243:50051", 100, "ge4,ge9,xe4")
add_ports("135.91.120.243:50051", 100, "ge4,ge9,xe4", "ge4")
destroy_vlan("135.91.120.243:50051", 100)

print(show_vlans("135.91.120.243:50051"))
set_pvlan("135.91.120.243:50051", 100, "ge4")
print(show_pvlans("135.91.120.243:50051"))
