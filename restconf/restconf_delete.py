import requests
from requests.auth import HTTPBasicAuth
import json
from urllib3 import disable_warnings
from getpass import getpass

#disable warnings
disable_warnings()

#Ask for the devices and credentials:
no_of_devices = int(input("Enter the number of devices you want to modify config on: "))

for devices in range(no_of_devices):
    ip = input("Enter the IP address: ")
    username = input("Enter the username: ")
    password = getpass("Enter the password: ")

    int_name = input("Enter the interface name you want to delete: ")

    base = f"https://{ip}/restconf/data"

    #Pass the credentials to HTTPBasicAuth, define url and headers
    cred = HTTPBasicAuth(username=username, password=password)
    headers = {"Accept": "application/yang-data+json", "Content-type": "application/yang-data+json"}
    url = f"{base}/ietf-interfaces:interfaces/interface={int_name}"

    #Execute the request
    request = requests.delete(url=url, auth=cred, headers=headers, verify=False)

    #print the response objects
    if request.status_code in (200, 201, 204):
        print(f"YAY!! Deleted Successfully. The status code is {request.status_code}")
    elif request.status_code == 404:
        print(f"\nAhh! Interface {int_name} not found (already deleted)!\nThe status code is {request.status_code}")
    else:
        print(request.text)

