from django.conf.urls import url
from . import views

app_name = 'marketplace'

urlpatterns = [
	url(r'^login/$', views.login_user, name="login_user"),
	url(r'^authenticate_user/$', views.authenticate_user, name="authenticate_user"),
	url(r'^logout/$', views.logout_user, name="logout_user"),
	url(r'^$', views.login_user, name='login_user'),
	url(r'^new_user/$', views.new_user, name='new_user'),
	url(r'^create_user/$', views.create_user, name='create_user'),
	url(r'^home/(?P<user_id>[0-9]+)$', views.home, name='home'),	
]