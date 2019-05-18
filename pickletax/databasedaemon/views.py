from django.http import HttpResponse
from django.views import View
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import string
import random
from pickletax import settings

app_email = settings.EMAIL_HOST_USER
dmitryi_verification_code = "Ural_4_gays!"
dmitryi_emails = [
	"discherbinin_1@edu.hse.ru"
]


class PickleTaxStatusCodes:
	authorization_ok = 200
	authorization_not_ok = 400
	verification_ok = 200
	verification_not_ok = 400
	unexpected_server_error = 500


def log_message(request, logger):
	try:
		logger.info("message logging - " + request.body.decode("utf-8"))
	except BaseException as error:
		logger.info("error section")
		logger.error("in log_message - " + error.__str__())


def generate_dmitryi_verification_code():
	code = list(dmitryi_verification_code)
	number = random.randint(3, dmitryi_verification_code.__len__() - 3)
	positions = []
	previous_position = 0
	for i in range(number):
		current_position = random.randint(previous_position, dmitryi_verification_code.__len__() - 1)
		positions.append(current_position)
		previous_position = current_position
	for position in positions:
		code[position] = code[position].capitalize()
	return "".join(code)


def generate_verification_code(email):
	# if is_dmitryi(email):
	# 	return generate_dmitryi_verification_code()
	code_length = 6
	letters = string.ascii_letters
	# return "".join(random.choice(letters) for i in range(code_length))
	return "aaa"


def get_institution_id(email):
	institutions = Institution.objects.all()
	for institution in institutions:
		if re.search(institution.email_domain, email) is not None:
			return institution


def get_unexpected_server_error(error, logger):
	logger.error("unexpected server error - " + error.__str__())
	return {"unexpected server error": error.__str__()}, PickleTaxStatusCodes.unexpected_server_error


def is_dmitryi(email):
	if email in dmitryi_emails:
		return True
	return False


def get_classroom_types():
	classroom_types = []
	for classroom_type in Classroom._type:
		classroom_types.append(classroom_type[0])
	return classroom_types


def get_max_lesson_number(user_email):
	return User.objects.get(email = user_email).institution_ID.max_lesson_number


def get_institution_structure(user_email):
	campuses = Campus.objects.filter(institution_ID = User.objects.get(email = user_email).institution_ID)
	campus_array = []
	for campus in campuses:
		classrooms = Classroom.objects.filter(campus_ID = campus)
		classroom_array = []
		for classroom in classrooms:
			classroom_array.append(
				{
					"name": classroom.number,
					"campus_name": campus.name,
					"type": classroom.type
				}
			)
		campus_array.append(
			{
				"name": campus.name,
				"classrooms": classrooms
			}
		)
	return campus_array


class AuthorizationView(View):
	from logs.logger import authorization_logger as logger
	http_method_names = ["post"]

	def authorize(self, body):
		try:
			new_user = User.objects.get(email = body["email"])
		except ObjectDoesNotExist:
			new_user = User(
				email = body["email"],
				institution_ID = get_institution_id(body["email"])
			)
		except BaseException as error:
			return get_unexpected_server_error(error, self.logger)

		try:
			new_user.save()
		except ValidationError as error:
			self.logger.error(error)
			response = {"error": error.__str__()}
			status_code = PickleTaxStatusCodes.authorization_not_ok
		except BaseException as error:
			response, status_code = get_unexpected_server_error(error, self.logger)
		else:
			verification_code = generate_verification_code(body["email"])
			new_user.email_verification_code = verification_code
			self.logger.debug("verification code - " + verification_code.__str__())
			new_user.save()
			message = "This is verification code:" + verification_code + "\nPlease, entry it in corresponding field in the app."
			send_mail(
				subject = "Verification in PickleTax",
				message = message,
				from_email = app_email,
				recipient_list = [body["email"]]
			)
			response = {"status": "authorization ok"}
			status_code = PickleTaxStatusCodes.authorization_ok

		return response, status_code

	def verificate(self, body):
		try:
			user = User.objects.get(email = body["email"])
			if body["verification_code"] == user.email_verification_code:
				# todo: also returning database is required
				response = {
					"status": "verification ok",
					"campuses": get_institution_structure(user.email),
					"classrooms_types": get_classroom_types(),
					"max_lesson_number": get_max_lesson_number(user.email)
				}
				return response, PickleTaxStatusCodes.verification_ok
			return {"status": "verification not ok"}, PickleTaxStatusCodes.verification_not_ok
		except BaseException as error:
			self.logger.debug("123")
			return get_unexpected_server_error(error, self.logger)

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		log_message(request, self.logger)
		body = json.loads(request.body)
		if body.get("city") is not None:
			response, status_code = self.authorize(body)
		else:
			response, status_code = self.verificate(body)

		return HttpResponse(json.dumps(response), content_type = "application/json", status = status_code)


class DaemonView(View):
	http_method_names = ["get"]

	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello, world!")
