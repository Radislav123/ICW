from django.test import TestCase
from logs.logger import unit_tests_logger as logger
import requests
import json


address = "http://127.0.0.1:8000/pickletax/databasedaemon/"
authorization = address + "authorization/"


print("\nAuthorization test starts.")
try:
	# json_str = str(
	#	{
	#		"city": "Москва".encode("utf-8"),
	#		"email": "testemail@edu.hse.ru"
	#	}
	# )
	response = requests.post(
		url = authorization,
		data = b'{"city":"\xd0\x9c\xd0\xbe\xd1\x81\xd0\xba\xd0\xb2\xd0\xb0","email":"cher-di@mail.ru"}'
	)
	assert response.status_code == 250, "authorization post-method failed " + response.__str__()

	print("Authorization tests passed successfully.")
except AssertionError as error:
	logger.error(error)
	print("Authorization tests were not passed.")
