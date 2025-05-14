from . import views
from django.urls import path,include
from django.contrib import admin

urlpatterns = [
    path("users/", views.create_user, name="user"),
    #path('users/',include('django.contrib.auth.urls')),
    path("", views.home, name="home"),          
    path("entrada/", views.entrada, name="entrada"),  
    path("base/", views.base, name="base"),
]