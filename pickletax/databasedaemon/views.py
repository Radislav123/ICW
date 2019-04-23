from django.http import HttpResponse


def main_view(request):
	return HttpResponse("It is databasedaemon main view")
