from ncclient import manager
from xml.dom.minidom import parseString
from getpass import getpass

#connect to IOSXE4 device using manager.connect()

no_of_devices = int(input("Enter the number of devices you want to get config: "))

for i in range(no_of_devices):

    hostname = input("Enter the hostname or IP address: ")
    username = input("Enter the username: ")
    password = getpass("Enter the password: ")

    with manager.connect(
        host = hostname,
        port = "830",
        username = username,
        password = password,
        hostkey_verify = "false"
    ) as m:
        print("NETCONF connection established with IOSXE4")
        print("Fetching server capabilities: ")
        #Fetch server capabilities:
        for cap in m.server_capabilities:
            print(cap)

