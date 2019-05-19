from databasedaemon import models


exec(open('databasedaemon\\databasefilling\\cleardatabase.py', encoding = 'utf-8').read())
exec(open('databasedaemon\\databasefilling\\create_institutions_and_campuses.py', encoding = 'utf-8').read())
exec(open('databasedaemon\\databasefilling\\create_classrooms_and_activities.py', encoding = 'utf-8').read())


new_user = models.User(
	email = "testemail@edu.hse.ru",
	institution_ID = models.Institution.objects.get(
		name = "Национальный исследовательский университет «Высшая школа экономики» (НИУ ВШЭ)"
	),
	city = "Москва"
)
new_user.save()

print("Basics were filled in database.")
