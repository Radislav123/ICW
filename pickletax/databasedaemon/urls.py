from django.conf.urls import url
from . import views


app_name = 'databasedaemon'
urlpatterns = [
	url(r'^$', views.main_view, name = 'main_view')
]
