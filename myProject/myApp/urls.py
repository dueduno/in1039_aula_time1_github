from . import views
from django.urls import path

urlpatterns = [
    path("",views.home, name="home"),
    path("historico",views.historico, name="historico"),
    path("favoritos",views.favoritos, name="favoritos"),
]

