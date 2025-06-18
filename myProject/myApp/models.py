from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

from django.db import models

class Cliente(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Outros campos do seu Cliente, por exemplo:
    # telefone = models.CharField(max_length=20, blank=True, null=True)
    # endereco = models.CharField(max_length=255, blank=True, null=True)

    # Adicione este campo para a foto de perfil
    foto = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/')

    def __str__(self):
        return f'Perfil de {self.user.username}'

    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome

class Administrador(Cliente):
    cnpj = models.CharField(max_length=18, unique=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)
    try:
        instance.cliente.save() # Acessa o profile através do related_name 'cliente'
    except Cliente.DoesNotExist:


# Se você não tem um modelo Cliente para perfil, crie um:
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Estacionamento(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    total_vagas = models.IntegerField()
    vagas_disponiveis = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nome

class Possui(models.Model):
    funcionario = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    estacionamento = models.ForeignKey(Estacionamento, on_delete=models.CASCADE)

class Vaga(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    estacionamento = models.ForeignKey(Estacionamento, on_delete=models.CASCADE, related_name='vagas')
    disponivel = models.BooleanField(default=True) # Pode ser default=False se criada apenas ao reservar.
    active = models.BooleanField(default=False) 
    
    id_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  
        null=True,                  
        blank=True,                 
        related_name='vagas_reservadas' 
    )
    
    def __str__(self):
        if self.active and self.id_user:
            return f"Vaga {self.codigo} ({self.estacionamento.nome}) - Reservada por: {self.id_user.username} (ATIVA)"
        elif self.id_user:
            return f"Vaga {self.codigo} ({self.estacionamento.nome}) - Histórico de Reserva para: {self.id_user.username} (INATIVA)"
        return f"Vaga {self.codigo} ({self.estacionamento.nome}) - Inativa/Disponível para nova reserva"
    

    def __str__(self):
        if self.id_user:
            return f"Vaga {self.codigo} ({self.estacionamento.nome}) - Reservada por: {self.id_user.username}"
        return f"Vaga {self.codigo} ({self.estacionamento.nome}) - Disponível"

class Contem(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    estacionamento = models.ForeignKey(Estacionamento, on_delete=models.CASCADE)

class Reserva(models.Model):
    hora_entrada = models.DateTimeField()
    codigo = models.CharField(max_length=20)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    hora_saida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.codigo


class Historico(models.Model):
    """
    Registra quantas vezes um usuário específico parou em um estacionamento específico.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contagem_estacionamentos')
    estacionamento = models.ForeignKey(Estacionamento, on_delete=models.CASCADE, related_name='contagem_usuarios')
    num_paradas = models.IntegerField(default=0) # Contador de vezes que o usuário parou neste estacionamento

    class Meta:
        # Garante que um usuário só tenha um contador por estacionamento
        unique_together = ('user', 'estacionamento')
        verbose_name = "Contador de Paradas no Estacionamento"
        verbose_name_plural = "Contadores de Paradas nos Estacionamentos"

    def __str__(self):
        return f"{self.user.username} parou {self.num_paradas} vezes em {self.estacionamento.nome}"