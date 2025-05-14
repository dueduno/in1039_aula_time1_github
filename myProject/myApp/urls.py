from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),          
    path("entrada/", views.entrada, name="entrada"),  
    path("base/", views.base, name="base"),
]