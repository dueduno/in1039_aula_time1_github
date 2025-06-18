# myApp/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Manter esta URL se 'esqueci_senha' for uma página diferente
    # ou se for usada para algum outro propósito além da redefinição por e-mail.
    # Se a intenção é que "Esqueci a senha" sempre leve ao fluxo de e-mail,
    # esta linha pode ser removida e os links podem apontar para 'esqueci_senha_email'.
    path('esqueci_senha/', views.esqueci_senha, name='esqueci_senha'),

    path('', views.home, name='home'),
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
    path('trocar_imagem_perfil/', views.trocar_imagem_perfil, name='trocar_imagem_perfil'),

    # REMOVIDA A LINHA ABAIXO para evitar duplicação
    # path('esqueci_senha_email/',views.esqueci_senha_email,name='esqueci_senha_email'),

    # URL para a página onde o usuário insere o e-mail para redefinição
    # Esta é a URL que deve ser usada para iniciar o fluxo de redefinição de senha do Django.
    path('esqueci_senha_email/', auth_views.PasswordResetView.as_view(
        template_name='esqueci_senha_email.html',
        email_template_name='password_reset_email_custom.html', # Você vai criar este
        subject_template_name='password_reset_subject_custom.txt', # Você vai criar este
        success_url='/password_reset_done_custom/' # Redireciona após o e-mail ser enviado
    ), name='esqueci_senha_email'),

    # URL para a página que informa que o e-mail de redefinição foi enviado
    path('password_reset_done_custom/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done_custom.html' # Você vai criar este
    ), name='password_reset_done_custom'),

    # URL para a página onde o usuário define a nova senha
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm_custom.html', # Você vai criar este
        success_url='/password_reset_complete_custom/' # Redireciona após a senha ser alterada
    ), name='password_reset_confirm'), # Mantenha este nome padrão, é importante para o link do e-mail

    # URL para a página de confirmação de redefinição de senha completa
    path('password_reset_complete_custom/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete_custom.html' # Você vai criar este
    ), name='password_reset_complete_custom'),
]