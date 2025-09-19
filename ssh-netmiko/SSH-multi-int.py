from netmiko import ConnectHandler
from getpass import getpass

ip = input("Enter the device IP to SSH: ")
username = input("Enter your username: ")
password = getpass("Enter your  password: ")

router_details = {
    'ip':ip,
    'username':username,
    'password':password,
    'device_type':'cisco_ios'
}

ssh = ConnectHandler(**router_details)
print("SSH Connection Established with the device Successfully..!")

user_input = int(input("Enter the number of interfaces that you wish to configure: "))

for abc in range(0, user_input):

    int_name = input("Enter the interface name: ")
    int_ip = input("Enter the interface IP Address: ")
    int_mask = input("Enter the interface subnet mask: ")
    int_desc = input("Enter the interface description: ")

    commands = [f'interface {int_name}',  f'ip address {int_ip} {int_mask}', 'no shutdown', f'desc {int_desc}']

    int_configs = ssh.send_config_set(commands)
    print(int_configs)

    int_details = ssh.send_command(input("Enter the show command that you wish to run for verification: "))
    print(int_details)

ssh.save_config()
ssh.disconnect()