from rest_framework import serializers
from .models import Cliente, Administrador, Estacionamento, Vaga, Reserva, Historico, Possui, Contem, Favorito
from django.contrib.auth.models import User

# Nenhum serializer precisa de mudança, exceto o FavoritoSerializer.
# Apenas garantimos que o EstacionamentoSerializer existe e está completo.

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
    # Usar '__all__' já é suficiente para incluir todos os campos necessários.
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


class FavoritoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Favorito.
    Agora, ele aninha o objeto completo do Estacionamento.
    """
    # ATUALIZAÇÃO: Esta linha substitui as antigas 'estacionamento_nome' e 'estacionamento'.
    # Ela usa o EstacionamentoSerializer para incluir todos os detalhes do estacionamento relacionado.
    estacionamento = EstacionamentoSerializer(read_only=True)
    
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Favorito
        # ATUALIZAÇÃO: O campo 'fields' agora é mais limpo e poderoso.
        fields = [
            'id', 
            'usuario_username', 
            'estacionamento', # Este campo agora contém o objeto completo do estacionamento
            'data_criacao'
        ]
