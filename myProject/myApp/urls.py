from django.urls import path
from . import views

urlpatterns = [
    path('esqueci_senha/',views.esqueci_senha,name='esqueci_senha'),
    path('', views.home, name='home'),
    # path('base/', views.base, name='base'),
    path('entrada/', views.entrada, name='entrada'),
    path('register/', views.create_user, name='register'),
    path('users/login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('mapa/', views.mapa, name='mapa'),
    path('criar_estacionamento/', views.criar_estacionamento, name='criar_estacionamento'),
    path('reservar_vaga/', views.reservar_vaga, name='reservar_vaga'),
    path('sair-vaga/', views.sair_da_vaga, name='sair_vaga'),
]