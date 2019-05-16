import databasedaemon.models as models

exec(open('databasedaemon\\cleardatabase.py', encoding = 'utf-8').read())

new_institution = models.Institution(
	name = "Национальный исследовательский университет «Высшая школа экономики» (НИУ ВШЭ)",
	class_type = "пара"
)
new_institution.save()

new_campus = models.Campus(
	institution_ID = models.Institution.objects.get(
		name = "Национальный исследовательский университет «Высшая школа экономики» (НИУ ВШЭ)"
	),
	name = "Московский институт электроники и математики НИУ ВШЭ (МИЭМ НИУ ВШЭ)",
	city = "Москва",
	address = "Таллинская улица, 34"
)
new_campus.save()

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
	mail = "testemail@edu.hse.ru",
	institution_ID = models.Institution.objects.get(
		name = "Национальный исследовательский университет «Высшая школа экономики» (НИУ ВШЭ)"
	),
)

print("Basics were filled in database.")
