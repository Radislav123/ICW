from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json


def log_message(request, logger):
	try:
		body = json.loads(request.body)
		logger.log(10, "тест")
		logger.log(20, "тест")
		logger.debug("тест")
		logger.error("тест")
	except BaseException as error:
		logger.error(error)


class AuthorizationView(View):
	from logs.logger import authorization_logger as logger
	http_method_names = ["post"]


	@csrf_exempt
	def post(self, request, *args, **kwargs):
		log_message(request, self.logger)
		response = {"something": "from authorization"}
		return HttpResponse(json.dumps(response), content_type = "application/json", status = 250)


class DaemonView(View):
	http_method_names = ["get"]

	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello, world!")
