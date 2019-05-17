from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views import View
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import string
import random

app_email = "pickletax@mail.ru"
dmitryi_verification_code = "Ural_for_gays!"
dmitryi_emails = [
	"cherdiadm@gmail.com",
	"cher-di@mail.ru",
	"ya.cher-di@yandex.ru"
]


def log_message(request, logger):
	try:
		logger.info(request.body.decode("utf-8"))
	except BaseException as error:
		logger.info("error section")
		logger.error("in log_message - " + error.__str__())


def generate_verification_code(email):
	if is_dmitryi(email):
		return dmitryi_verification_code
	code_length = 6
	letters = string.ascii_letters
	return "".join(random.choice(letters) for i in range(code_length))


def get_institution_id(email):
	try:
		pass
	except:
		pass


def get_unexpected_error(error):
	return {"unexpected error": error.__str__()}, 550


def is_dmitryi(email):
	if email in dmitryi_emails:
		return True
	return False


class AuthorizationView(View):
	from logs.logger import authorization_logger as logger
	http_method_names = ["post"]

	def authorize(self, body):
		response: dict
		status_code: int
		new_user: User

		try:
			new_user = User.objects.get(email = body["email"])
		except ObjectDoesNotExist:
			# todo: write sending to email
			new_user = User(
				email = body["email"],
				institution_ID = get_institution_id(body["email"])
			)
			response = {}
			status_code = 250
		except BaseException as error:
			self.logger.error(error)
			response, status_code = get_unexpected_error(error)

		try:
			new_user.save()
		except ValidationError as error:
			self.logger.error(error)
			response = {}
			status_code = 450
		except BaseException as error:
			self.logger.error(error)
			response, status_code = get_unexpected_error(error)
		else:
			verification_code = generate_verification_code(body["email"])
			new_user.email_verification_code = verification_code
			new_user.save()
			send_mail(
				subject = "Verification in PickleTax",
				message = "This is your verification code: %s\nPlease, entry it in corresponding field in the app.",
				from_email = app_email,
				recipient_list = [body["email"]]
			)

		return response, status_code

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		log_message(request, self.logger)
		body = json.loads(request.body)
		response: dict
		status_code: int
		if body.get("city") is not None:
			response, status_code = self.authorize(body)
		else:
			# todo: write
			pass

		response = {"something": "from authorization"}
		return HttpResponse(json.dumps(response), content_type = "application/json", status = status_code)


class DaemonView(View):
	http_method_names = ["get"]

	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello, world!")
