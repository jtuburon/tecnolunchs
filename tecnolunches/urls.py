from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^welcome$', views.welcome, name='welcome'),
    url(r'^logout$', views.logout, name='logout'),
	url(r'^groups/$', views.groups, name='groups'),
	url(r'^group_details/(?P<group_id>[0-9]+)/$', views.show_group_details, name='group_details'),
	url(r'^queues/$', views.queues, name='queues'),
	url(r'^menues/$', views.menues, name='menues'),
	url(r'^menues/new/$', views.new_menu, name='new_menu'),
	url(r'^menues/save/$', views.save_menu, name='save_menu'),
	url(r'^menues/find/(?P<menu_id>[0-9]+)/$', views.find_menu, name='find_menu'),
	url(r'^menues/setavailable/(?P<menu_id>[0-9]+)/(?P<menu_status>(true|false))/$', views.set_menu_availability, name='set_menu_availability'),
	url(r'^admin/$', views.admin, name='admin'),
	url(r'^admin/save_gral_settings/$', views.save_gral_settings, name='save_gral_settings'),
	url(r'^admin/today/$', views.today, name='today'),
	url(r'^admin/today/group_member/set_accomplishment/(?P<group_member_id>[0-9]+)/(?P<group_member_status>(true|false))/$', views.set_groupmember_accomplishment, name='set_groupmember_accomplishment'),
]