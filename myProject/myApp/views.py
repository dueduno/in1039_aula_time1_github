from django.shortcuts import render
from .models import Cliente, Administrador, Estacionamento, Possui, Vaga, Contem, Reserva

def home(request):
    cliente = Cliente.objects.all()
    administrador = Administrador.objects.all()
    estacionamento=Estacionamento.objects.all()
    possui=Possui.objects.all()
    vaga=Vaga.objects.all()
    contem=Contem.objects.all()
    reserva=Reserva.objects.all()
    return render(request, "myApp/home.html",context={"cliente":cliente}) #Perguntar na aula se eu posso passar uma lista de dicionarios 
