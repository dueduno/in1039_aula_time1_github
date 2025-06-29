from rest_framework import serializers
from .models import Cliente, Administrador, Estacionamento, Vaga, Reserva, Historico, Possui, Contem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__' 

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__' 

class EstacionamentoSerializer(serializers.ModelSerializer):
    vagas = serializers.StringRelatedField(many=True, read_only=True) 

    class Meta:
        model = Estacionamento
        fields = '__all__'

class VagaSerializer(serializers.ModelSerializer):
    id_user = UserSerializer(read_only=True) 
    estacionamento_nome = serializers.CharField(source='estacionamento.nome', read_only=True)

    class Meta:
        model = Vaga
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    vaga_codigo = serializers.CharField(source='vaga.codigo', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'

class HistoricoSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    estacionamento_nome = serializers.CharField(source='estacionamento.nome', read_only=True)

    class Meta:
        model = Historico
        fields = '__all__'


class PossuiSerializer(serializers.ModelSerializer):
    funcionario_nome = serializers.CharField(source='funcionario.nome', read_only=True)
    estacionamento_nome = serializers.CharField(source='estacionamento.nome', read_only=True)

    class Meta:
        model = Possui
        fields = '__all__'

class ContemSerializer(serializers.ModelSerializer):
    vaga_codigo = serializers.CharField(source='vaga.codigo', read_only=True)
    estacionamento_nome = serializers.CharField(source='estacionamento.nome', read_only=True)

    class Meta:
        model = Contem
        fields = '__all__'