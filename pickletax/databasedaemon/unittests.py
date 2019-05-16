from django.test import TestCase
from logs.logger import unit_tests_logger as logger
import requests
import json


address = "http://127.0.0.1:8000/pickletax/databasedaemon/"
authorization = address + "authorization/"


print("\nAuthorization test starts.")
try:
	response = requests.post(
		url = authorization,
		json = json.dumps(
			{
				"city": "Москва",
				"email": "testemail@edu.hse.ru"
			},
			# ensure_ascii = False
		)
	)
	assert response.status_code == 250, "authorization post-method failed " + response.__str__()

	print("Authorization tests passed successfully.")
except AssertionError as error:
	logger.error(error)
	print("Authorization tests were not passed.")
