from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Cliente, Administrador, Estacionamento, Possui, Vaga, Contem, Reserva
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # cliente = Cliente.objects.filter(nome = "joao").all()
    cliente = Cliente.objects.all()
    administrador = Administrador.objects.all()
    estacionamento=Estacionamento.objects.all()
    possui=Possui.objects.all()
    vaga=Vaga.objects.all()
    contem=Contem.objects.all()
    reserva=Reserva.objects.all()

    context = {
        "cliente":cliente,
        "administrador":administrador,
        "estacionamento":estacionamento,
        "possui":possui,
        "vagas":vaga,
        "contem":contem,
        "reserva":reserva,
    }

    return render(request, "home.html",context=context)

@login_required
def base(request):
    # cliente = Cliente.objects.filter(nome = "joao").all()
    cliente = Cliente.objects.all()
    administrador = Administrador.objects.all()
    estacionamento=Estacionamento.objects.all()
    possui=Possui.objects.all()
    vaga=Vaga.objects.all()
    contem=Contem.objects.all()
    reserva=Reserva.objects.all()

    context = {
        "cliente":cliente,
        "administrador":administrador,
        "estacionamento":estacionamento,
        "possui":possui,
        "vagas":vaga,
        "contem":contem,
        "reserva":reserva,
    }

    return render(request, "base.html",context=context)


@login_required
def entrada(request):
    # cliente = Cliente.objects.filter(nome = "joao").all()
    cliente = Cliente.objects.all()
    administrador = Administrador.objects.all()
    estacionamento=Estacionamento.objects.all()
    possui=Possui.objects.all()
    vaga=Vaga.objects.all()
    contem=Contem.objects.all()
    reserva=Reserva.objects.all()

    context = {
        "cliente":cliente,
        "administrador":administrador,
        "estacionamento":estacionamento,
        "possui":possui,
        "vagas":vaga,
        "contem":contem,
        "reserva":reserva,
    }

    return render(request, "entrada.html",context=context)

def create_user(request):
    if request.method=="POST":
        user = User.objects.create_user(
            request.POST["username"],
            request.POST["email"],
            request.POST["password"]
            )
        user.save
        return redirect("home")
    return render(request,"register.html",context={"action":"Adicionar"})



def login_user(request):
    if request.method=="POST":
        user=authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
            )
        if user!=None:
            login(request,user)
        else:
            return render(request,"login.html",context={"error_msg":"Usuário não existe"})

        if request.user.is_authenticated:
            return redirect("home")
        return render(request,"login.html",context={"error_msg":"Usuário não pode ser autenticado"})
    return render(request,"login.html")

def logout_user(request):
    logout(request)
    return redirect("login")