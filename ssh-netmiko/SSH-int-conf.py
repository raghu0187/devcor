from netmiko import ConnectHandler

R1 = {
    "device_type":"cisco_ios",
    "ip":"192.168.1.32",
    "username":"admin",
    "password":"cisco"
}

ssh = ConnectHandler(**R1)
print("Connection with router R1 eshtablished successfully!")

int_name = input("Enter the interface name: ")
int_ip = input("Enter the IP address: ")
int_mask = input("Enter the subnet mask: ")
int_desc = input("Enter the interface description: ")

commands = ["interface " + int_name, "ip address " + int_ip + " " + int_mask, "desc "+ int_desc, "no shutdown"]
int_conf = ssh.send_config_set(commands)
print(int_conf)

int_details = ssh.send_command("sh ip int br")
print(int_details)

ssh.save_config()
