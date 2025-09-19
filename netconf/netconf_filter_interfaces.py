from ncclient import manager
from xml.dom.minidom import parseString
from getpass import getpass
from xmltodict import parse

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
        print("Fetching filtered inerfaces config: ")
        
        #Fetch filtered config only related to interfaces:

        filter = """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            </interfaces>
        </filter>
        """

        int_filter = m.get_config(source="running", filter=filter).data_xml
        #print(result)

        #Convert XML into pretty output
        prettyprint = parseString(int_filter).toprettyxml()

        #Convert XML data into Dict
        xml_to_dict = parse(prettyprint)
        #print(xml_to_dict)

        int_dict_list = xml_to_dict["data"]["interfaces"]["interface"]
        #print(int_dict_list)

        for interface in int_dict_list:

            try:
                int_desc = interface["description"]
            except:
                int_desc = "not yet configured..!"

            #print(f"\nYour interface {interface['name']}'s description is {int_desc}")

            file = open("/home/student/Desktop/DEVCOR-DEVEX/DEVCOR Scripts/NETCONF/test.txt", "a")

            file.write(f"\nYour interface {interface['name']}'s description is {int_desc}")

            file.close()



