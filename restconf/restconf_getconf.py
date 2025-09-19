import requests
from requests.auth import HTTPBasicAuth
import json
from urllib3 import disable_warnings
from getpass import getpass

#disable warnings
disable_warnings()

#Ask for user credentials
xe_user = input("Enter the username: ")
xe_pass = getpass("Enter the password: ")

#Pass the credentials to HTTPBasicAuth, define url and headers
cred = HTTPBasicAuth(username = xe_user, password = xe_pass)
xe_url = "https://10.255.1.105/restconf/data/ietf-interfaces:interfaces"
xe_headers = {"Accept": "application/yang-data+json"}

#execute the request
request = requests.get(url=xe_url, auth=cred, headers=xe_headers, verify=False)

#print the response objects
print(f"Status code is {request.status_code}")

raw_json = json.loads(request.text)
pretty_json = json.dumps(raw_json, indent=4)
print(pretty_json)