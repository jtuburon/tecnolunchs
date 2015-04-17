from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^welcome$', views.welcome, name='welcome'),
    url(r'^logout$', views.logout, name='logout'),
]