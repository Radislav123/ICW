from databasedaemon import models
import random

from django.core.exceptions import ValidationError


def generate_classrooms_1(campus_1):
	new_classrooms_1 = []
	number = random.randint(15, 25)
	i = 10
	while i <= number:
		i += 1
		new_classrooms_1.append(
			models.Classroom(
				campus_ID = campus_1,
				number = "1" + i.__str__(),
				seat_number = i
			)
		)
	return new_classrooms_1


def generate_classrooms_2(campus_2):
	new_classrooms_2 = []
	number = random.randint(15, 25)
	i = 10
	while i <= number:
		i += 1
		new_classrooms_2.append(
			models.Classroom(
				campus_ID = campus_2,
				number = "2" + i.__str__(),
				seat_number = i,
				type = "лаборатория"
			)
		)
	return new_classrooms_2


def generate_classrooms_3(campus_3):
	new_classrooms_3 = []
	number = random.randint(15, 25)
	i = 10
	while i <= number:
		i += 1
		new_classrooms_3.append(
			models.Classroom(
				campus_ID = campus_3,
				number = "3" + i.__str__(),
				seat_number = i
			)
		)
	return new_classrooms_3


def generate_classrooms_4(campus_4):
	new_classrooms_4 = []
	number = random.randint(15, 25)
	i = 10
	while i <= number:
		i += 1
		new_classrooms_4.append(
			models.Classroom(
				campus_ID = campus_4,
				number = "4" + i.__str__(),
				seat_number = i
			)
		)
	return new_classrooms_4


def generate_classrooms_5(campus_5):
	new_classrooms_5 = []
	number = random.randint(15, 25)
	i = 10
	while i <= number:
		i += 1
		new_classrooms_5.append(
			models.Classroom(
				campus_ID = campus_5,
				number = "5" + i.__str__(),
				seat_number = i,
				type = "лекционная"
			)
		)
	return new_classrooms_5


def generate_classrooms(campus_0):
	new_classrooms_0 = generate_classrooms_1(campus_0)
	new_classrooms_0.extend(generate_classrooms_2(campus_0))
	new_classrooms_0.extend(generate_classrooms_3(campus_0))
	new_classrooms_0.extend(generate_classrooms_4(campus_0))
	new_classrooms_0.extend(generate_classrooms_5(campus_0))
	return new_classrooms_0


def generate_classroom_activities(campus_a, classroom_number_a):
	new_activities = []
	number = campus.institution_ID.max_lesson_number
	for i in range(1, number + 1):
		vacant = "свободна"
		if random.randint(1, 5) > 4:
			vacant = "занята"
		new_activity = models.ClassroomActivity(
			campus_ID = campus_a,
			classroom_number = classroom_number_a,
			number = i,
			vacant = vacant
		)
		new_activities.append(new_activity)
	return new_activities


campuses = models.Campus.objects.all()
try:
	for campus in campuses:
		new_classrooms = generate_classrooms(campus)
		for classroom in new_classrooms:
			classroom.save()
			new_classroom_activities = generate_classroom_activities(campus, classroom)
			for classroom_activity in new_classroom_activities:
				classroom_activity.save()
except ValidationError as error:
	print(error)
