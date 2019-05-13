from django.conf.urls import url
from . import views


app_name = 'databasedaemon'
urlpatterns = [
	url(r'^$', views.Greeter.as_view(), name = 'where can i this name see?'),
	url(r'authorization/$', views.Authorization.as_view(), name = 'authorization view')
]
