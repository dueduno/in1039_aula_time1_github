from . import views
from django.urls import path,include
from django.contrib import admin

urlpatterns = [
    path('criar-estacionamento/', views.criar_estacionamento, name='criar_estacionamento'),
    path('mapa/', views.mapa, name='mapa'),
    path('users/change_password/',views.change_password,name='change_password'),
    path("users/", views.create_user, name="user"),
    path("users/login/", views.login_user, name="login"),
    path("users/logout/", views.logout_user, name="logout"),
    #path('users/',include('django.contrib.auth.urls')),
    path("", views.home, name="home"),          
    path("entrada/", views.entrada, name="entrada"),  
    path("base/", views.base, name="base"),
]