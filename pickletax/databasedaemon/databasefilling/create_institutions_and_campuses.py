from databasedaemon import models

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
	),
	models.Campus(
		institution_ID = models.Institution.objects.get(
			name = "Национальный исследовательский университет «Высшая школа экономики» (НИУ ВШЭ)"
		),
		name = "Пермский кампус федерального государственного автономного образовательного учреждения высшего образования «Национальный исследовательский университет «Высшая школа экономики»",
		city = "Пермь",
		address = "Пермь, ул. Студенческая, 38"
	)
]
for campus in new_campuses:
	campus.save()
