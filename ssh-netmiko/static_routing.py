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

user_choice = int(input("Welcome to the Router Configuration Utility\nWhat would you like to configure: \n1. Interfaces Configs\n2. Static Routing\nPlease make a choice: "))

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

else:
    print("Please Try Again! This is an invalid")