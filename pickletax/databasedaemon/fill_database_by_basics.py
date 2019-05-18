import databasedaemon.models as models

exec(open('databasedaemon\\cleardatabase.py', encoding = 'utf-8').read())

new_institution = models.Institution(
	name = "Национальный исследовательский университет «Высшая школа экономики» (НИУ ВШЭ)",
	email_domain = "edu.hse",
	class_type = "пара"
)
new_institution.save()

new_campuses = [
	models.Campus(
		institution_ID = models.Institution.objects.get(
			name = "Национальный исследовательский университет «Высшая школа экономики» (НИУ ВШЭ)"
		),
		name = "Московский институт электроники и математики НИУ ВШЭ (МИЭМ НИУ ВШЭ)",
		city = "Москва",
		address = "Таллинская улица, 34"
	),
	models.Campus(
		institution_ID = models.Institution.objects.get(
			name = "Национальный исследовательский университет «Высшая школа экономики» (НИУ ВШЭ)"
		),
		name = "факультет экономики, Международный институт экономики и финансов, Базовая кафедра МакКинзи и Ко",
		city = "Москва",
		address = "Москва, ул. Шаболовка, д. 26, стр. 3, 4, 5, 9"
	)
]
for campus in new_campuses:
	campus.save()

new_classrooms = [
	models.Classroom(
		campus_ID = models.Campus.objects.get(
			name = "Московский институт электроники и математики НИУ ВШЭ (МИЭМ НИУ ВШЭ)"
		),
		number = "410",
		seat_number = 150,
		type = "лекционная",
	),
	models.Classroom(
		campus_ID = models.Campus.objects.get(
			name = "Московский институт электроники и математики НИУ ВШЭ (МИЭМ НИУ ВШЭ)"
		),
		number = "204",
		seat_number = 30,
	),
	models.Classroom(
		campus_ID = models.Campus.objects.get(
			name = "Московский институт электроники и математики НИУ ВШЭ (МИЭМ НИУ ВШЭ)"
		),
		number = "223",
		seat_number = 30,
		type = "лаборатория",
	)
]
for classroom in new_classrooms:
	classroom.save()
	for i in range(1, 10):
		new_classroom_activity = models.ClassroomActivity(
			campus_ID = models.Campus.objects.get(
				name = "Московский институт электроники и математики НИУ ВШЭ (МИЭМ НИУ ВШЭ)"
			),
			classroom_number = classroom,
			number = i
		)
		new_classroom_activity.save()

new_user = models.User(
	email = "testemail@edu.hse.ru",
	institution_ID = models.Institution.objects.get(
		name = "Национальный исследовательский университет «Высшая школа экономики» (НИУ ВШЭ)"
	),
)
new_user.save()

print("Basics were filled in database.")
