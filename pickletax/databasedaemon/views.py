from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json


class AuthorizationView(View):
	from logs.logger import authorization_logger as logger
	http_method_names = ["post"]

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		try:
			self.logger.debug("")
			self.logger.debug("post message")
			self.logger.debug(type(request.body))
			self.logger.debug(request.body)

			body = json.loads(request.body)
			self.logger.debug(type(body))
			self.logger.debug(body)
			self.logger.debug("")
		except BaseException as error:
			self.logger.error(error)
		response = {"something": "from authorization"}
		return HttpResponse(json.dumps(response), content_type = "application/json", status = 250)


class DaemonView(View):
	http_method_names = ["get"]

	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello, world!")
