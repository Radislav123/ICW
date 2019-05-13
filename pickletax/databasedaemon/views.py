import json
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class Greeter(View):
	http_method_names = ["get", "post"]

	def get(self, request, *args, **kwargs):
		response = {"method": "get"}
		return HttpResponse(json.dumps(response), content_type = "application/json", status = 250)

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		response = {"method": "post"}
		return HttpResponse(json.dumps(response), content_type = "application/json", status = 251)


class Authorization(View):
	http_method_names = ["get"]

	def get(self, request, *args, **kwargs):
		return HttpResponse(status = 250)
