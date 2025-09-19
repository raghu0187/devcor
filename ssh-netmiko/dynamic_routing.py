from netmiko import ConnectHandler
from getpass import getpass

routers = {
    "R1":"192.168.1.32",
    "R2":"192.168.1.33",
    "R3":"192.168.1.34"
}

print(routers)

user_choice = input("Enter the name of the router, you want to configure: ")
user_choice = user_choice.upper()
ip_add = routers[user_choice]

username = input("Enter your username: ")
password = getpass("Enter your password: ")

router_details = {
    'ip':ip_add,
    'username':username,
    'password':password,
    'device_type':'cisco_ios'
}

ssh = ConnectHandler(**router_details)
print("SSH Connection Established successfully...!!")

user_choice = int(input("Welcome to the Router Configuration Utility\nWhat would you like to configure: \n1. Interfaces Configs\n2. Static Routing\n3. EIGRP\n4. OSPF\nPlease make a choice: "))

if user_choice == 1:
    print("You have selected Interface Configurations...")

    number_of_int = int(input("How many interfaces would you like to configure: "))

    for int_conf in range(0, number_of_int):
        int_name = input("Enter the interface name: ")
        int_ip = input("Enter the interface IP : ")
        int_mask = input("Enter the interface subnet mask: ")

        commands = [f'interface {int_name}', f'ip address {int_ip} {int_mask}', 'desc Configured using Python', 'no shutdown']
        int_configs = ssh.send_config_set(commands)
        print(int_configs)

elif user_choice == 2:
    print("You have selected Static Routes Configurations...")

    number_of_routes = int(input("How many routes do you wish to configure: "))

    for static_conf in range(0, number_of_routes):
        network_id = input("Enter the destination network ID: ")
        subnet_m = input("Enter the destination subnet mask: ")
        next_hop = input("Enter the next hop address or exit interface: ")

        commands = [f'ip route {network_id} {subnet_m} {next_hop}']
        static_configs = ssh.send_config_set(commands)
        print(static_configs)

elif user_choice == 3:
    print("You have selected EIGRP Configurations...")

    eigrp_as = input("Enter the EIGRP AS Number: ")
    number_of_networks = int(input("How many networks would you like to configure under EIGRP: "))

    for eigrp_conf in range(0, number_of_networks):
        network_id = input("Enter the network ID: ")
        wildcard_m = input("Enter the wildcard mask: ")

        commands = [f'router eigrp {eigrp_as}', 'no auto-summary', f'network {network_id} {wildcard_m}']
        eigrp_configs = ssh.send_config_set(commands)
        print(eigrp_configs)

    eigrp_details = ssh.send_command("show run | sec eigrp")
    print(eigrp_details)

elif user_choice == 4:
    print("You have selected OSPF Configurations...")

    ospf_process = input("Enter the OSPF Process ID: ")
    number_of_routes = int(input("Enter the number of networks that you wish to add: "))

    for ospf_conf in range(0, number_of_routes):
        network_id = input("Enter the network ID: ")
        wildcard_m = input("Enter the network wildcard mask: ")
        area_id = input("Enter the area ID: ")

        commands = [f'router ospf {ospf_process}', f'network {network_id} {wildcard_m} area {area_id}']
        ospf_configs = ssh.send_config_set(commands)
        print(ospf_configs)

    ospf_details = ssh.send_command("show run | sec ospf")
    print(ospf_details)

        
else:
    print("Please Try Again! This is an invalid")

ssh.save_config()
ssh.disconnect()