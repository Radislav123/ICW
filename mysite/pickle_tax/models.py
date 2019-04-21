from django.db import models

from django.db import models
from django.utils import timezone


class Campus(models.Model):
	ID = models.IntegerField(primary_key = True)
	name = models.CharField()
	# todo: should it be validated?
	city = models.CharField()
	address = models.CharField()
	info = models.CharField(blank = True)


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
	campusID = models.ForeignKey(Campus, to_field = Campus.ID, on_delete = models.PROTECT)
	# sometimes, appears classrooms with number 210a, for example.
	number = models.CharField(primary_key = True)
	seatNumber = models.IntegerField()
	accessRight = models.CharField(choices = __access_rights, default = "free")
	type = models.CharField(choices = __type, default = "seminary")
	info = models.CharField(blank = True)


class ClassroomActivity(models.Model):
	__vacant = (
		("free", "free"),
		("reserved", "reserved"),
		("occupied", "occupied")
	)
	campusID = models.ForeignKey(Campus, to_field = Campus.ID, on_delete = models.PROTECT)
	classroomNumber = models.ForeignKey(Classroom, to_field = Classroom.number, on_delete = models.PROTECT)
	# todo: write time validating(timeFinish > timeStart; timeFinish - timeStart == const)
	timeStart = models.TimeField()
	timeFinish = models.TimeField()
	vacant = models.CharField(choices = __vacant, default = "free")
	info = models.CharField(blank = True)


class User(models.Model):
	__status = (
		("student", "student"),
		("teacher", "teacher"),
		("redactor", "redactor"),
		("server", "server")
	)
	# todo: use EmailValidator from django
	mail = models.EmailField()
	# todo: maybe, it should be encrypted?
	password = models.CharField()
	# todo: validate to scale from -100 to 100
	goodFaithIndex = models.IntegerField()
	mainCampusID = models.ForeignKey(Campus, to_field = Campus.ID, on_delete = models.PROTECT)
	status = models.CharField(choices = __status, default = "student")
