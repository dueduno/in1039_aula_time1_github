from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome

class Administrador(Cliente):
    cnpj = models.CharField(max_length=18, unique=True)

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
    codigo = models.CharField(max_length=20)
    estacionamento = models.ForeignKey(Estacionamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo

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
