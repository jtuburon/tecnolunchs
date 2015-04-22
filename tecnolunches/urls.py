from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^welcome$', views.welcome, name='welcome'),
    url(r'^logout$', views.logout, name='logout'),
	url(r'^groups/$', views.groups, name='groups'),
	url(r'^group_details/(?P<group_id>[0-9]+)/$', views.show_group_details, name='group_details'),
	url(r'^queues/$', views.queues, name='queues'),
	url(r'^admin/$', views.admin, name='admin'),
	url(r'^admin/save_gral_settings/(?P<group_size>[0-9]+)/$', views.save_gral_settings, name='save_gral_settings'),
	url(r'^admin/today/$', views.today, name='today'),
]