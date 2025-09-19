from netmiko import ConnectHandler
from getpass import getpass

router_ip = open(r"D:\CODE\devices.txt", "r")

#r - reading
#w - writing
#a - appending

username_r = input("Enter your username: ")
password_r = getpass("Enter your password: ")

for ip_add in router_ip:
    router_details = {
        'ip':ip_add,
        'username':username_r,
        'password':password_r,
        'device_type':'cisco_ios'
    }

    ssh = ConnectHandler(**router_details)
    print("SSH Connection established successfully with " + ip_add)

    commands = open(r"D:\CODE\commands.txt", "r")
    output_file = open(r"D:\CODE\output.txt", "a")
    output_file.write("The below information is fetched from " + ip_add)

    for show_commands in commands:
        details = ssh.send_command(show_commands)
        output_file.write("\n\n" + details + "\n\n")

    output_file.close()
    commands.close()

    print("Output was exported successfully...!")


router_ip.close()