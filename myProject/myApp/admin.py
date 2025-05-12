from django.contrib import admin
from .models import Cliente, Administrador, Estacionamento, Possui, Vaga, Contem, Reserva

admin.site.register(Cliente)
admin.site.register(Administrador)
admin.site.register(Estacionamento)
admin.site.register(Possui)
admin.site.register(Vaga)
admin.site.register(Contem)
admin.site.register(Reserva)

# Register your models here.
