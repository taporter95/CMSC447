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
	#url(r'^home/(?P<user_id>[0-9]+)$', views.home, name='home'),	
	url(r'^home/$', views.home, name='home'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^create_post/$', views.create_post, name='create_post'),
	url(r'^view_post/(?P<post_id>[0-9]+)$', views.view_post, name='view_post'),
	url(r'^update_post/(?P<post_id>[0-9]+)$', views.update_post, name='update_post'),
	url(r'^delete_post/(?P<post_id>[0-9]+)$', views.delete_post, name='delete_post'),
	url(r'^checkout/(?P<post_id>[0-9]+)$', views.checkout, name='checkout'),
	url(r'^buy/(?P<post_id>[0-9]+)$', views.buy, name='buy'),

	]