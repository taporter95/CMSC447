from django.conf.urls import url
from . import views

app_name = 'marketplace'

urlpatterns = [
	url(r'^login/$', views.login_user, name="login_user"),
	url(r'^authenticate_user/$', views.authenticate_user, name="authenticate_user"),
	url(r'^logout/$', views.logout_user, name="logout_user"),
	url(r'^$', views.home, name='home'),
	url(r'^new_user/$', views.new_user, name='new_user'),
	url(r'^create_user/$', views.create_user, name='create_user'),
	url(r'^delete_account/$', views.delete_account, name='delete_account'),
	url(r'^home/$', views.home, name='home'),
	url(r'^search_results/$', views.search_results, name='search_results'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^update_profile/$', views.update_profile, name='update_profile'),
	url(r'^create_post/$', views.create_post, name='create_post'),
	url(r'^view_post/(?P<post_id>[0-9]+)$', views.view_post, name='view_post'),
	url(r'^update_post/(?P<post_id>[0-9]+)$', views.update_post, name='update_post'),
	url(r'^delete_post/(?P<post_id>[0-9]+)$', views.delete_post, name='delete_post'),
	url(r'^checkout/(?P<post_id>[0-9]+)$', views.checkout, name='checkout'),
	url(r'^buy/(?P<post_id>[0-9]+)$', views.buy, name='buy'),
	url(r'^transactions/$', views.transactions, name='transactions'),
	url(r'^view_transaction/(?P<transaction_id>[0-9]+)$', views.view_transaction, name='view_transaction'),
	url(r'^relist_post/(?P<transaction_id>[0-9]+)$', views.relist_post, name='relist_post'),
	url(r'^complete_transaction/(?P<transaction_id>[0-9]+)$', views.complete_transaction, name='complete_transaction'),
	]