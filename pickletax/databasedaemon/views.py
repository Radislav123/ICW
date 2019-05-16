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
			# without ensure_ascii
			self.logger.debug(json.loads(request.body).encode("utf-8").decode("unicode-escape"))
			# with ensure_ascii
			# self.logger.debug(request.body.decode("unicode-escape"))
		except BaseException as error:
			self.logger.error(error)
		response = {"something": "from authorization"}
		return HttpResponse(json.dumps(response), content_type = "application/json", status = 250)


class DaemonView(View):
	http_method_names = ["get", "post"]
	from logs.logger import daemon_view_logger as logger

	def get(self, request, *args, **kwargs):
		# todo: to realise update functionality
		response = {"method": "get"}
		return HttpResponse(json.dumps(response), content_type = "application/json", status = 250)

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		# todo: to realise authorization and classroom status update functionality
		# authorization
		logger.info("post request")
		try:
			new_user = User(
				mail = "testemail@edu.hse.ru",
				institution_ID = Institution.objects.get(ID = 1),
				status = "студент"
			)
		except ValidationError as error:
			logger.error(error)
		except BaseException as error:
			logger.error(error)
		response = {}
		status_code = 251
		new_user.save()

		# email code verification

		# classroom status update

		return HttpResponse(json.dumps(response), content_type = "application/json", status = status_code)
