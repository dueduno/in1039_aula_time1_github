from django.shortcuts import render
from .models import Cliente, Administrador, Estacionamento, Possui, Vaga, Contem, Reserva

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

def historico(request):
     return render(request, "historico.html")