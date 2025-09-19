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
    
    choose_int_type=int(input("1. Logical\n2. Physical\nChoose interface type you want to configure[1/2]: "))

    #map the choice to the interface type and parameters:
    if choose_int_type==1:
        interface_type="softwareLoopback"
    elif choose_int_type==2:
        interface_type="ethernetCsmacd"
    else:
        print("Wrong input, please try again!!")

    int_name=input("Enter the interface name: ")
    int_desc=input("Enter the description: ")
    int_ip=input("Enter the IP add you want to configure: ")
    int_mask=input("Enter the subnet mask you want to enter: ")

    #Create the interface

    create_interface_xml=f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{int_name}</name>
                <description>{int_desc}</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:{interface_type}</type>
                <enabled>true</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{int_ip}</ip>
                        <netmask>{int_mask}</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """

    #Merge the config
    try:
        with open_session() as m:
            merge=m.edit_config(create_interface_xml, target="running")
            print("Created interface: \n", merge)
    except RPCError as e:
        print("RPC Error")
        print("Type:", e.type)
        print("Tag: ", e.tag)
        print("Message: ", e.message)











