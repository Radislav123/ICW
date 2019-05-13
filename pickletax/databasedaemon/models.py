import re
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import dateparse


info_length = 500
name_length = 100
choice_length = 20


# here validators are represented
def city_validator(value):
	cities = []
	if value not in cities:
		raise ValidationError(message = "%(city)s is not in out city list.", params = {"city": value})


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


def mail_validator(value):
	regex = re.compile(r"\w{1,40}@\w{1,10}.\w{1,10}.?\w{,5}")
	if re.fullmatch(regex, value) is None:
		raise ValidationError(
			message = "%(value)s is not a valid email(please entry email witch fits example pattern - \"something@edu.hse.ru\".",
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


# todo: write _str_ methods
# here models are represented
class Institution(models.Model):
	__classType = (
		("simple class", "simple class"),
		("doubled class", "doubled class")
	)
	ID = models.AutoField(primary_key = True)
	name = models.CharField(max_length = name_length)
	class_type = models.CharField(max_length = choice_length, choices = __classType, default = "doubled class")


class Campus(models.Model):
	ID = models.AutoField(primary_key = True)
	institution_ID = models.ForeignKey(to = Institution, to_field = 'ID', on_delete = models.PROTECT)
	name = models.CharField(max_length = name_length, blank = True)
	city = models.CharField(max_length = name_length, validators = [city_validator])
	address = models.CharField(max_length = name_length)
	info = models.CharField(max_length = choice_length, blank = True)


class Classroom(models.Model):
	__access_rights = (
		("free", "free"),
		("teacher is required", "teacher is required"),
		("for stuff only", "for stuff only")
	)
	__type = (
		("lecture", "lecture"),
		("seminary", "seminary"),
		("laboratory", "laboratory"),
		("for stuff", "for stuff")
	)
	campus_ID = models.ForeignKey(to = Campus, to_field = 'ID', on_delete = models.PROTECT)
	# sometimes, appears classrooms with number 210a, for example.
	number = models.CharField(max_length = choice_length, primary_key = True, validators = [classroom_number_validator])
	seat_number = models.IntegerField(validators = [classroom_seat_number_validator])
	access_rights = models.CharField(max_length = choice_length, choices = __access_rights, default = "free")
	type = models.CharField(max_length = choice_length, choices = __type, default = "seminary")
	info = models.CharField(max_length = info_length, blank = True)


class ClassroomActivity(models.Model):
	__vacant = (
		("free", "free"),
		("reserved", "reserved"),
		("occupied", "occupied")
	)
	campus_ID = models.ForeignKey(Campus, to_field = 'ID', on_delete = models.PROTECT)
	classroom_umber = models.ForeignKey(Classroom, to_field = 'number', on_delete = models.PROTECT)
	number = models.IntegerField(validators = [class_number_validator])
	vacant = models.CharField(max_length = choice_length, choices = __vacant, default = "free")
	info = models.CharField(max_length = info_length, blank = True)


class User(models.Model):
	__status = (
		("student", "student"),
		("teacher", "teacher"),
		("redactor", "redactor"),
		("server", "server")
	)
	mail = models.CharField(max_length = name_length, validators = [mail_validator])
	good_faith_index = models.IntegerField()
	main_campus_ID = models.ForeignKey(Campus, to_field = 'ID', on_delete = models.PROTECT)
	status = models.CharField(max_length = choice_length, choices = __status, default = "student")

