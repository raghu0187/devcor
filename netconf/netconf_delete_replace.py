from ncclient import manager
from xml.dom.minidom import parseString
from ncclient.operations import RPCError
from getpass import getpass

#connect to IOSXE4 device using manager.connect()

no_of_devices = int(input("Enter the number of devices you want to get config: "))

for i in range(no_of_devices):

    hostname = input("Enter the hostname or IP address: ")
    username = input("Enter the username: ")
    password = getpass("Enter the password: ")

    def open_session():
        return manager.connect(
            host=hostname,
            port=830,
            username=username,
            password=password,
            hostkey_verify=False, # don't verify server host key
            allow_agent=False,    # don't use SSH agent
            look_for_keys=False,  # Don't search for private keys
            timeout=30            # Give up after 30s
        )
    
    with open_session() as m:
        print("Connected!!")
        for cap in m.server_capabilities:
            if "ietf-interfaces" in cap or "Cisco-IOS-XE" in cap:
                print(cap)
    
    #If you want to delete/replace the existing config

    user_choice = int(input("\n1. Replace the description\n2. Delete the interface\nMake your choice[1/2]: "))

    if user_choice == 1:
        int_name = input("Enter the interface name: ")
        replace_desc = input("Enter the new description: ")

        replace_desc_xml=f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{int_name}</name>
                    <description operation = "replace">{replace_desc}</description>
                </interface>
            </interfaces>
        </config>
        """
        with open_session() as m:
            replace=m.edit_config(replace_desc_xml, target="running")
            print(f"Replaced interface description is : {replace_desc}", replace)

    elif user_choice == 2:
        delete_int_name=input("Enter the interface you want to delete: ")

        delete_interface_xml=f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation = "delete">
                    <name>{delete_int_name}</name>
                </interface>
            </interfaces>
        </config>
        """

        with open_session() as m:
            delete=m.edit_config(delete_interface_xml, target="running")
            print(f"Deleted interface is : {delete_int_name}", delete)

    else:
        print("wrong input, please try again!!")
        exit(1)

 









