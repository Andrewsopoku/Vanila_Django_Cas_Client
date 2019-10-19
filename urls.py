from django.conf.urls import url

from vanila_djangocore_cas import views

__author__ = 'andrews'

urlpatterns = [
    url(r'^accounts/signin',views.login, name="app-signin"),
    url(r'^accounts/signout',views.logout, name="app-signout"),

    ]