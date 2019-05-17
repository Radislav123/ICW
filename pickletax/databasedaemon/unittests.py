from django.test import TestCase
from logs.logger import unit_tests_logger as logger
import requests
import json


address = "http://ec2-18-225-6-37.us-east-2.compute.amazonaws.com:9090/pickletax/databasedaemon/"
authorization = address + "authorization/"


print("\nAuthorization test starts.")
try:
	response = requests.post(
		url = authorization,
		data = b'{"city":"\xd0\x9c\xd0\xbe\xd1\x81\xd0\xba\xd0\xb2\xd0\xb0","email":"cher-di@mail.ru"}'
	)
	assert response.status_code == 250, "authorization post-method failed " + response.__str__()

	print("Authorization tests passed successfully.")
except AssertionError as error:
	logger.error(error)
	print("Authorization tests were not passed.")
