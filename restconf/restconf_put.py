import requests
from requests.auth import HTTPBasicAuth
import json
from urllib3 import disable_warnings
from getpass import getpass

#disable warnings
disable_warnings()

#Ask for the devices and credentials:
no_of_devices = int(input("Enter the number of devices you want to create config on: "))

for devices in range(no_of_devices):
    ip = input("Enter the IP address: ")
    username = input("Enter the username: ")
    password = getpass("Enter the password: ")

    #map the choice to the interface type and parameters:
    choose_int_type=int(input("1. Logical\n2. Physical\nChoose interface type you want to configure[1/2]: "))
    if choose_int_type==1:
        interface_type="softwareLoopback"
    elif choose_int_type==2:
        interface_type="ethernetCsmacd"
    else:
        print("Wrong input, please try again!!")

    int_name = input("Enter the interface name you want to create: ")
    description = input("Enter the description you want to create: ")
    int_ip = input("Enter the new IP address you want to configure: ")
    int_mask = input("Enter the new mask you want to configure: ")
    base = f"https://{ip}/restconf/data"

    #Pass the credentials to HTTPBasicAuth, define url and headers
    cred = HTTPBasicAuth(username=username, password=password)
    headers = {"Accept": "application/yang-data+json", "Content-type": "application/yang-data+json"}
    url = f"{base}/ietf-interfaces:interfaces/interface={int_name}"
    print(url)
    payload = {
        "ietf-interfaces:interface": {
            "name": int_name,
            "description": description,
            "type": f"iana-if-type:{interface_type}",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": int_ip,
                        "netmask": int_mask
                    }
                ]
            }
        }
    }

    #Execute the request
    request = requests.put(url=url, auth=cred, headers=headers, data=json.dumps(payload), verify=False)

    #print the response objects
    if request.status_code in (200, 201, 204):
        print(f"YAY!! Successful. The status code is {request.status_code}")
    else:
        print(request.text)

