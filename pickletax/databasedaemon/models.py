from django.db import models


infoLength = 500
nameLength = 100
choiceLength = 20


class Campus(models.Model):
	ID = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = nameLength)
	# todo: should it be validated?
	city = models.CharField(max_length = nameLength)
	address = models.CharField(max_length = nameLength)
	info = models.CharField(max_length = choiceLength, blank = True)


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
	campusID = models.ForeignKey(to = Campus, to_field = 'ID', on_delete = models.PROTECT)
	# sometimes, appears classrooms with number 210a, for example.
	number = models.CharField(max_length = choiceLength, primary_key = True)
	seatNumber = models.IntegerField()
	accessRight = models.CharField(max_length = choiceLength, choices = __access_rights, default = "free")
	type = models.CharField(max_length = choiceLength, choices = __type, default = "seminary")
	info = models.CharField(max_length = infoLength, blank = True)


class ClassroomActivity(models.Model):
	__vacant = (
		("free", "free"),
		("reserved", "reserved"),
		("occupied", "occupied")
	)
	campusID = models.ForeignKey(Campus, to_field = 'ID', on_delete = models.PROTECT)
	classroomNumber = models.ForeignKey(Classroom, to_field = 'number', on_delete = models.PROTECT)
	# todo: write time validating(timeFinish > timeStart; timeFinish - timeStart == const)
	timeStart = models.TimeField()
	timeFinish = models.TimeField()
	vacant = models.CharField(max_length = choiceLength, choices = __vacant, default = "free")
	info = models.CharField(max_length = infoLength, blank = True)


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
	password = models.CharField(max_length = choiceLength)
	# todo: validate to scale from -100 to 100
	goodFaithIndex = models.IntegerField()
	mainCampusID = models.ForeignKey(Campus, to_field = 'ID', on_delete = models.PROTECT)
	status = models.CharField(max_length = choiceLength, choices = __status, default = "student")
