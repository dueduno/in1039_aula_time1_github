from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Cliente, Administrador, Estacionamento, Possui, Vaga, Contem, Reserva
import random

@login_required
def home(request):
    cliente = Cliente.objects.all()
    administrador = Administrador.objects.all()
    estacionamento = Estacionamento.objects.all()
    possui = Possui.objects.all()
    vaga = Vaga.objects.all()
    contem = Contem.objects.all()
    reserva = Reserva.objects.all()

    context = {
        "cliente": cliente,
        "administrador": administrador,
        "estacionamento": estacionamento,
        "possui": possui,
        "vagas": vaga,
        "contem": contem,
        "reserva": reserva,
    }

    return render(request, "home.html", context=context)

@login_required
def base(request):
    cliente = Cliente.objects.all()
    administrador = Administrador.objects.all()
    estacionamento = Estacionamento.objects.all()
    possui = Possui.objects.all()
    vaga = Vaga.objects.all()
    contem = Contem.objects.all()
    reserva = Reserva.objects.all()

    context = {
        "cliente": cliente,
        "administrador": administrador,
        "estacionamento": estacionamento,
        "possui": possui,
        "vagas": vaga,
        "contem": contem,
        "reserva": reserva,
    }

    return render(request, "base.html", context=context)

@login_required
def entrada(request):
    cliente = Cliente.objects.all()
    administrador = Administrador.objects.all()
    estacionamento = Estacionamento.objects.all()
    possui = Possui.objects.all()
    vaga = Vaga.objects.all()
    contem = Contem.objects.all()
    reserva = Reserva.objects.all()

    context = {
        "cliente": cliente,
        "administrador": administrador,
        "estacionamento": estacionamento,
        "possui": possui,
        "vagas": vaga,
        "contem": contem,
        "reserva": reserva,
    }

    return render(request, "entrada.html", context=context)

def create_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST.get("confirm-password")

        if password != confirm_password:
            return render(request, "register.html", context={
                "action": "Criar",
                "error_msg": "As senhas não coincidem. Por favor, verifique."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", context={
                "action": "Criar",
                "error_msg": "Nome de usuário já está em uso."
            })
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", context={
                "action": "Criar",
                "error_msg": "E-mail já está em uso."
            })

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            return redirect("home")
        except Exception as e:
            return render(request, "register.html", context={
                "action": "Criar",
                "error_msg": f"Erro ao registrar: {str(e)}"
            })

    return render(request, "register.html", context={"action": "Criar"})

def login_user(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user is not None:
            login(request, user)
        else:
            return render(request, "login.html", context={"error_msg": "Usuário não pode ser autenticado"})

        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "login.html", context={"error_msg": "Usuário não pode ser autenticado"})
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("login")

def esqueci_senha(request):
    return render(request,'esqueci_senha_nova_senha')

@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")

        user = authenticate(username=request.user.username, password=current_password)
        if user is None:
            return render(request, "change_password.html", context={
                "error_msg": "Senha atual incorreta."
            })

        if new_password != confirm_new_password:
            return render(request, "change_password.html", context={
                "error_msg": "As novas senhas não coincidem."
            })

        try:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Senha alterada com sucesso!")
            return redirect("home")
        except Exception as e:
            return render(request, "change_password.html", context={
                "error_msg": f"Erro ao alterar a senha: {str(e)}"
            })

    return render(request, "change_password.html", context={})

@login_required
def mapa(request):
    estacionamentos = Estacionamento.objects.all()
    return render(request, 'mapa.html', {'estacionamentos': estacionamentos})

@login_required
def criar_estacionamento(request):
    if request.method == 'POST':
        try:
            Estacionamento.objects.create(
                nome=request.POST['nome'],
                endereco=request.POST['endereco'],
                total_vagas=int(request.POST['total_vagas']),
                vagas_disponiveis=int(request.POST['total_vagas']),
                preco=float(request.POST['preco'])
            )
            messages.success(request, 'Estacionamento cadastrado com sucesso!')
            return redirect('mapa')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    return render(request, 'criar_estacionamento.html')

@login_required
def reservar_vaga(request):
    if request.method == 'POST':
        try:
            estacionamento_id = request.POST.get('estacionamento_id')
            estacionamento = Estacionamento.objects.get(id=estacionamento_id)
            
            # Verificar se há vagas disponíveis
            if estacionamento.vagas_disponiveis <= 0:
                messages.error(request, 'Nenhuma vaga disponível neste estacionamento.')
                return redirect('mapa')
            
            # Decrementar vagas disponíveis
            estacionamento.vagas_disponiveis -= 1
            estacionamento.save()
            
            # Gerar um código aleatório para a vaga
            codigo_vaga = str(random.randint(1000, 9999))
            
            # Criar registro na tabela Vaga
            Vaga.objects.create(
                codigo=codigo_vaga,
                estacionamento=estacionamento
            )
            
            messages.success(request, f'Vaga reservada com sucesso! Código: {codigo_vaga}')
            return redirect('mapa')
        except Estacionamento.DoesNotExist:
            messages.error(request, 'Estacionamento não encontrado.')
            return redirect('mapa')
        except Exception as e:
            messages.error(request, f'Erro ao reservar vaga: {str(e)}')
            return redirect('mapa')
    
    return redirect('mapa')