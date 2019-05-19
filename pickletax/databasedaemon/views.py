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
	user_status_update_ok = 200
	change_status_ok = 200
	change_status_not_ok = 400
	validation_error = 400
	unexpected_server_error = 500


def log_message(request, logger):
	try:
		logger.info("message logging - " + request.body.decode("utf-8"))
	except BaseException as error:
		logger.info("error section")
		logger.error("in log_message - " + error.__str__())


def get_institution_id(user_email):
	institutions = Institution.objects.all()
	for institution in institutions:
		if re.search(institution.email_domain, user_email) is not None:
			return institution


def get_unexpected_server_error(error, logger):
	logger.error("unexpected server error - " + error.__str__())
	return {"unexpected server error": error.__str__()}, PickleTaxStatusCodes.unexpected_server_error


def get_validation_error(error, logger):
	logger.error("validation error - " + error.__str__())
	return {"validation error": error.__str__()}, PickleTaxStatusCodes.validation_error


class AuthorizationView(View):
	from logs.logger import authorization_logger as logger
	http_method_names = ["post"]

	def get_max_lesson_number(self, user_email):
		return User.objects.get(email = user_email).institution_ID.max_lesson_number

	def get_classroom_types(self):
		classroom_types = []
		for classroom_type in Classroom._type:
			classroom_types.append(classroom_type[0])
		return classroom_types

	def get_institution_structure(self, user_email):
		campuses = Campus.objects.filter(
			institution_ID = get_institution_id(user_email),
			city = User.objects.get(email = user_email).city
		)
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
					"classrooms": classroom_array
				}
			)
		return campus_array

	def is_dmitryi(self, user_email):
		if user_email in dmitryi_emails:
			return True
		return False

	def generate_dmitryi_verification_code(self):
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

	def generate_verification_code(self, user_email):
		# if self.is_dmitryi(user_email):
		# 	return self.generate_dmitryi_verification_code()
		code_length = 6
		letters = string.ascii_letters
		# return "".join(random.choice(letters) for i in range(code_length))
		return "aaa"

	def authorize(self, body):
		try:
			new_user = User.objects.get(email = body["email"])
			new_user.city = body["city"]
		except ObjectDoesNotExist:
			new_user = User(
				email = body["email"],
				institution_ID = get_institution_id(body["email"]),
				city = body["city"]
			)
		except BaseException as error:
			return get_unexpected_server_error(error, self.logger)

		try:
			new_user.save()
		except ValidationError as error:
			response, status_code = get_validation_error(error, self.logger)
		except BaseException as error:
			response, status_code = get_unexpected_server_error(error, self.logger)
		else:
			verification_code = self.generate_verification_code(body["email"])
			new_user.email_verification_code = verification_code
			self.logger.debug("verification code - " + verification_code.__str__())
			new_user.save()
			message = "This is your verification code:" + verification_code
			message += "\nPlease, entry it in corresponding field in the app."
			message += "\nWe are not cheaters. There is our course work."
			message += "\nIf you are not expecting for this message, please ignore it."
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
				response = {
					"status": "verification ok",
					"campuses": self.get_institution_structure(user.email),
					"classrooms_types": self.get_classroom_types(),
					"max_lesson_number": self.get_max_lesson_number(user.email)
				}
				return response, PickleTaxStatusCodes.verification_ok
			return {"status": "verification not ok"}, PickleTaxStatusCodes.verification_not_ok
		except BaseException as error:
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


class UserStatusUpdateView(View):
	from logs.logger import status_update_logger as logger
	http_method_names = ["post"]

	def get_occupied_lessons(self, classroom):
		occupied_classroom_activities = ClassroomActivity.objects.filter(
			classroom_number = classroom,
			vacant = ClassroomActivity._vacant[2][0]
		)
		lessons = []
		for classroom_activity in occupied_classroom_activities:
			description = classroom_activity.info
			if description == "":
				description = "null"
			lessons.append(
				{
					"lesson_number": classroom_activity.number,
					"lesson_description": description
				}
			)
		return lessons

	def get_schedule(self, user_email):
		user = User.objects.get(email = user_email)
		campuses = Campus.objects.filter(
			institution_ID = user.institution_ID,
			city = user.city
		)
		campus_array = []
		for campus in campuses:
			classrooms = Classroom.objects.filter(campus_ID = campus)
			classroom_array = []
			for classroom in classrooms:
				classroom_array.append(
					{
						"name": classroom.number,
						"lessons": self.get_occupied_lessons(classroom)
					}
				)
			campus_array.append(
				{
					"name": campus.name,
					"classrooms_in_schedule": classroom_array
				}
			)
		return campus_array

	def post(self, request, *args, **kwargs):
		try:
			log_message(request, self.logger)
			response = {"campuses": self.get_schedule(json.loads(request.body)["email"])}
			status_code = PickleTaxStatusCodes.user_status_update_ok
		except BaseException as error:
			response, status_code = get_unexpected_server_error(error, self.logger)
		return HttpResponse(json.dumps(response), content_type = "application/json", status = status_code)


class StatusChangeView(View):
	from logs.logger import status_change_logger as logger
	http_method_names = ["post"]

	def change_classroom_status(self, body):
		campus = Campus.objects.get(name = body["campus_name"])
		classroom = Classroom.objects.get(number = body["classroom_name"], campus_ID = campus)
		classroom_activity = ClassroomActivity.objects.get(
			campus_ID = campus,
			classroom_number = classroom,
			number = body["lesson_number"]
		)
		if classroom_activity.vacant == body["new_classroom_status"]:
			if body["new_classroom_status"] == ClassroomActivity._vacant[2][0]:
				response = {"error": "classroom is already occupied"}
			else:
				response = {"error": "classroom is already free"}
			return response, PickleTaxStatusCodes.change_status_not_ok
		else:
			classroom_activity.vacant = body["new_classroom_status"]
			classroom_activity.info = body["description"]
		try:
			classroom_activity.save()
			response = {"something": "from change_classroom_status()"}
			status_code = PickleTaxStatusCodes.change_status_ok
		except ValidationError as error:
			response, status_code = get_validation_error(error, self.logger)
		except BaseException as error:
			response, status_code = get_unexpected_server_error(error, self.logger)

		return response, status_code

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		try:
			response, status_code = self.change_classroom_status(json.loads(request.body))
		except BaseException as error:
			response, status_code = get_unexpected_server_error(error, self.logger)
		return HttpResponse(json.dumps(response), content_type = "application/json", status = status_code)


class DaemonView(View):
	http_method_names = ["get"]

	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello, world!")
