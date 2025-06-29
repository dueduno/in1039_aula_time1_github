from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet, AdministradorViewSet, EstacionamentoViewSet,
    VagaViewSet, ReservaViewSet, HistoricoViewSet,
    PossuiViewSet, ContemViewSet, UserViewSet
)

# API
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'administradores', AdministradorViewSet)
router.register(r'estacionamentos', EstacionamentoViewSet)
router.register(r'vagas', VagaViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'historico', HistoricoViewSet)
router.register(r'possui', PossuiViewSet)
router.register(r'contem', ContemViewSet)
router.register(r'users', UserViewSet)

# Crie uma lista separada para as URLs do router.
# Elas não terão um prefixo aqui, o prefixo 'api/' será adicionado no urls.py principal.
api_router_urls = router.urls


urlpatterns = [
    path('esqueci_senha/', views.esqueci_senha, name='esqueci_senha'),
    path('home', views.home, name='home'),
    path('entrada/', views.entrada, name='entrada'),
    path('register/', views.create_user, name='register'),
    path('users/login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('mapa/', views.mapa, name='mapa'),
    path('criar_estacionamento/', views.criar_estacionamento, name='criar_estacionamento'),
    path('reservar_vaga/', views.reservar_vaga, name='reservar_vaga'),
    path('sair-vaga/', views.sair_da_vaga, name='sair_vaga'),
    path('botoes/', views.botoes, name='botoes'),
    path('perfil/', views.pagina_perfil, name='perfil'),
    path('politica_privacidade/', views.politica_privacidade, name='politica_privacidade'),
    path('termos-de-uso/', views.termos_de_uso, name='termos_de_uso'),
    path('suporte/', views.suporte, name='suporte'),
    path('favoritos/', views.favoritos, name='favoritos'),

    # --------------- REINICIAÇÃO DE SENHA DO DJANGO -----------------
    path('esqueci_senha_email/', auth_views.PasswordResetView.as_view(
        template_name='esqueci_senha_email.html',
        email_template_name='password_reset_email_custom.html',
        subject_template_name='password_reset_subject_custom.txt',
        success_url='/password_reset_done_custom/'
    ), name='esqueci_senha_email'),

    path('password_reset_done_custom/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done_custom.html'
    ), name='password_reset_done_custom'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm_custom.html',
        success_url='/password_reset_complete_custom/'
    ), name='password_reset_confirm'),

    path('password_reset_complete_custom/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete_custom.html'
    ), name='password_reset_complete_custom'),
]

# Adicione as URLs do router diretamente à lista urlpatterns
# O router.urls já é uma lista de URLs, então você pode concatenar
urlpatterns += api_router_urls