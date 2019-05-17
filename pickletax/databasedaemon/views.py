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
			self.logger.debug("post message")
			self.logger.debug(type(request.body))
			self.logger.debug(request.body)
			# without ensure_ascii
			# self.logger.debug(json.loads(request.body).encode("utf-8").decode("unicode-escape"))
			# with ensure_ascii
			# self.logger.debug(request.body.decode("unicode-escape"))
		except BaseException as error:
			self.logger.error(error)
		response = {"something": "from authorization"}
		return HttpResponse(json.dumps(response), content_type = "application/json", status = 250)


class DaemonView(View):
	http_method_names = ["get"]

	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello, world!")
