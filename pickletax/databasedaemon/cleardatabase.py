import databasedaemon.models as models


models.User.objects.all().delete()
models.ClassroomActivity.objects.all().delete()
models.Classroom.objects.all().delete()
models.Campus.objects.all().delete()
models.Institution.objects.all().delete()
print("Database was cleared successfully.")
