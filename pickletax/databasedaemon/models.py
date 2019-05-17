import re
from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist


info_length = 500
name_length = 100
choice_length = 20


# here validators are represented
def city_validator(value):
	cities = [
		"Москва",
		"Красноярск",
		"Казань"
	]
	if value not in cities:
		raise ValidationError(message = "%(city)s is not in our city list.", params = {"city": value})


def classroom_number_validator(value):
	regex = re.compile(r"\d+[a-zA-Z]{,3}")
	if not isinstance(value, str):
		raise ValidationError(
			message = "%(value)s: classroom_number_validator param is not str type.",
			params = {"value": value}
		)
	if re.fullmatch(regex, value) is None:
		raise ValidationError(message = "%(value)s is not a valid classroom number.", params = {"value": value})


def good_faith_index_validating(value):
	if value not in range(-100, 101):
		raise ValidationError(message = "%(value)s is not in range from -100 to 100.", params = {"value": value})


def email_validator(value):
	regex = re.compile(r"\w{1,40}@\w{1,10}.\w{1,10}.\w{,5}")
	if re.fullmatch(regex, value) is None:
		raise ValidationError(
			message = "%(value)s is not a valid email(please entry email witch fits example pattern - \"something@edu.hse.ru\".",
			params = {"value": value}
		)


def email_domain_validator(value):
	try:
		Institution.objects.get(email_domain = value)
	except ObjectDoesNotExist:
		pass
	else:
		raise ValidationError(
			message = "%(value)s email domain is already reserved or there is another problem.",
			params = {"value": value}
		)


def classroom_seat_number_validator(value):
	if value <= 0:
		raise ValidationError(
			message = "%(value)s is 0 or lower. Classroom can not contain so much seats.",
			params = {"value": value}
		)
	if value > 400:
		raise ValidationError(
			message = "%(value)s is too big(> 400). Classroom can not contain so much seats.",
			params = {"value": value}
		)


def class_number_validator(value):
	if value <= 0:
		raise ValidationError(
			message = "%(value)s is 0 or lower. The number of student class can not be less then 1st.",
			params = {"value": value}
		)
	if value > 400:
		raise ValidationError(
			message = "%(value)s is too big(> 12). The number of student class can not be more then 12th.",
			params = {"value": value}
		)


# here models are represented
class Institution(models.Model):
	_class_type = (
		("урок", "урок"),
		("пара", "пара")
	)
	ID = models.AutoField(primary_key = True)
	name = models.CharField(max_length = name_length)
	email_domain = models.CharField(max_length = choice_length, default = "hse", validators = [email_domain_validator])
	class_type = models.CharField(max_length = choice_length, choices = _class_type, default = "пара")
	max_lesson_number = models.IntegerField(default = 9)

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)


class Campus(models.Model):
	ID = models.AutoField(primary_key = True)
	institution_ID = models.ForeignKey(to = Institution, to_field = 'ID', on_delete = models.PROTECT)
	name = models.CharField(max_length = name_length, blank = True)
	city = models.CharField(max_length = name_length, validators = [city_validator])
	address = models.CharField(max_length = name_length)
	info = models.CharField(max_length = choice_length, blank = True)

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)


class Classroom(models.Model):
	_access_rights = (
		("свободный", "свободный"),
		("необходимость преподавателя", "необходимость преподавателя"),
		("только для сотрудников", "только для сотрудников")
	)
	_type = (
		("лекционная", "лекционная"),
		("семинарская", "семинарская"),
		("лаборатория", "лаборатория"),
		("для сотрудников", "для сотрудников")
	)
	campus_ID = models.ForeignKey(to = Campus, to_field = 'ID', on_delete = models.PROTECT)
	# sometimes, appears classrooms with number 210a, for example.
	number = models.CharField(max_length = choice_length, primary_key = True, validators = [classroom_number_validator])
	seat_number = models.IntegerField(validators = [classroom_seat_number_validator])
	access_rights = models.CharField(max_length = choice_length, choices = _access_rights, default = "свободный")
	type = models.CharField(max_length = choice_length, choices = _type, default = "семинарская")
	info = models.CharField(max_length = info_length, blank = True)

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)


class ClassroomActivity(models.Model):
	_vacant = (
		("свободна", "свободна"),
		("зарезервирована", "зарезервирована"),
		("занята", "занята")
	)
	campus_ID = models.ForeignKey(Campus, to_field = 'ID', on_delete = models.PROTECT)
	classroom_number = models.ForeignKey(Classroom, to_field = 'number', on_delete = models.PROTECT)
	number = models.IntegerField(validators = [class_number_validator])
	vacant = models.CharField(max_length = choice_length, choices = _vacant, default = "свободна")
	info = models.CharField(max_length = info_length, blank = True)

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)


class User(models.Model):
	_status = (
		("студент", "студент"),
		("преподаватель", "преподаватель"),
		("редактор", "редактор"),
		("сервер", "сервер")
	)
	email = models.CharField(max_length = name_length, validators = [email_validator])
	good_faith_index = models.IntegerField(default = 0)
	institution_ID = models.ForeignKey(Institution, to_field = 'ID', on_delete = models.PROTECT)
	status = models.CharField(max_length = choice_length, choices = _status, default = "студент")
	email_verification_code = models.CharField(max_length = choice_length, blank = True)

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)
