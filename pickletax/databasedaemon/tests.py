from django.test import TestCase
import requests
import json
import re


address = "http://127.0.0.1:8000/pickletax/databasedaemon/"

print("\nGreeter tests are starting")

assert requests.get(address).status_code == 250
assert requests.post(address).status_code == 251
assert requests.delete(address).status_code == 405
assert json.loads(requests.get(address).text) == {"method": "get"}
assert json.loads(requests.post(address).text) == {"method": "post"}

print("Greeter tests passed successfully")


print("\nAuthorization tests are starting")

assert requests.get(address + "authorization/").status_code == 250
assert requests.post(address + "authorization/").status_code == 405
assert requests.delete(address + "authorization/").status_code == 405

print("Authorization tests passed successfully")
