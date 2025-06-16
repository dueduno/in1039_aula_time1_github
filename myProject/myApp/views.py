import random
import traceback
from django.db import transaction 
from django.shortcuts import redirect, render # Adicionado render para funções existentes
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone 

# Importe seus modelos. Ajuste os caminhos conforme a estrutura do seu projeto.
from .models import Cliente, Administrador, Estacionamento, Possui, Vaga, Contem, Reserva, Historico
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash # Adicionado para as funções de autenticação

# Funções existentes (home, entrada, create_user, login_user, etc.)
# Mantenha as funções abaixo exatamente como no seu código original.

#@login_required
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

    return render(request, 'home.html', context=context)

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

def pagina_perfil(request):
    return render(request,'perfil.html')

def logout_user(request):
    logout(request)
    return redirect("home")

def botoes(request):
    return render(request, 'botoes.html')

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
    reserva_ativa_do_usuario = None 

    # Buscar apenas vagas ativas para o usuário
    if request.user.is_authenticated:
        reserva_ativa_do_usuario = Vaga.objects.filter(id_user=request.user, active=True).first()
    
    context = {
        'estacionamentos': estacionamentos,
        'reserva_ativa_do_usuario': reserva_ativa_do_usuario,
    }
    return render(request, 'mapa.html', context)

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

def reservar_vaga(request):
    """
    Função para reservar uma vaga em um estacionamento.
    Cria um novo registro de Vaga (representando a ocupação atual).
    """
    if request.method == 'POST':
        try:
            estacionamento_id = request.POST.get('estacionamento_id')
            
            # Bloqueia a linha do estacionamento para evitar condições de corrida em ambientes multi-usuário.
            estacionamento = Estacionamento.objects.select_for_update().get(id=estacionamento_id)
            
            # --- Validação: Verificar se o usuário já possui uma vaga ativa (ocupada) ---
            if Vaga.objects.filter(id_user=request.user, active=True).exists():
                messages.error(request, 'Você já possui uma vaga ativa. Por favor, saia dela antes de reservar outra.')
                return redirect('mapa')

            # Verificar se há vagas disponíveis no estacionamento (contador geral)
            if estacionamento.vagas_disponiveis <= 0:
                messages.error(request, 'Nenhuma vaga disponível neste estacionamento.')
                return redirect('mapa')
            
            # Decrementar vagas disponíveis no estacionamento
            estacionamento.vagas_disponiveis -= 1
            estacionamento.save()
            
            # Gerar um código aleatório único para a vaga (reserva)
            # Um loop simples para garantir a unicidade do código.
            codigo_vaga = ''
            while True:
                codigo_vaga = str(random.randint(1000, 9999))
                # Verifica se o código já existe em Vaga (qualquer estado)
                if not Vaga.objects.filter(codigo=codigo_vaga).exists():
                    break
            
            # Criar um novo registro na tabela Vaga (representando a ocupação ATUAL)
            # Este registro será DELETADO quando o usuário sair.
            Vaga.objects.create(
                codigo=codigo_vaga,
                estacionamento=estacionamento,
                id_user=request.user,  # Associar a vaga ao usuário logado
                disponivel=False,      # Esta instância de vaga está ocupada
                active=True            # Marcar esta vaga como atualmente ativa
            )
            
            messages.success(request, f'Vaga reservada com sucesso! Código: {codigo_vaga}')
            return redirect('mapa')
            
        except Estacionamento.DoesNotExist:
            messages.error(request, 'Estacionamento não encontrado.')
            return redirect('mapa')
        except Exception as e:
            # Captura erros gerais e os exibe para o usuário
            print(f"Erro detalhado em reservar_vaga: {e}") 
            traceback.print_exc() 
            messages.error(request, f'Erro ao reservar vaga: {str(e)}')
            return redirect('mapa')
    
    # Se a requisição não for POST, redireciona para o mapa
    return redirect('mapa')

@login_required 
def sair_da_vaga(request):
    """
    Função para o usuário sair da vaga.
    Deleta o registro da Vaga e incrementa o contador no Historico.
    """
    if request.method == 'POST':
        try:
            # Garante que todas as operações dentro do bloco sejam bem-sucedidas
            # ou todas sejam revertidas (atomicidade).
            with transaction.atomic():
                # 1. Encontrar a vaga ATIVA do usuário logado.
                # Use select_for_update para evitar problemas de concorrência.
                vaga_a_liberar = Vaga.objects.select_for_update().get(id_user=request.user, active=True)
                
                estacionamento = vaga_a_liberar.estacionamento
                
                if estacionamento is None:
                    messages.error(request, 'Erro: A vaga não está associada a um estacionamento válido.')
                    return redirect('mapa')

                # 2. Incrementar vagas disponíveis no estacionamento
                estacionamento.vagas_disponiveis += 1
                estacionamento.save()
                
                # 3. --- NOVO: Atualizar o Historico ---
                # Busca ou cria o registro de contador para este usuário e estacionamento
                historico_contador, created = Historico.objects.get_or_create(
                    user=request.user, 
                    estacionamento=estacionamento,
                    defaults={'num_paradas': 0} # Se for criado, começa com 0
                )
                historico_contador.num_paradas += 1 # Incrementa o contador
                historico_contador.save() # Salva o contador atualizado
                
                # 4. --- VOLTANDO AO COMPORTAMENTO ORIGINAL: Deletar a vaga ---
                # O registro de Vaga (que representava a ocupação ativa) é removido.
                vaga_a_liberar.delete()
            
            messages.success(request, 'Você saiu da vaga com sucesso! Ela agora está disponível para outros usuários.')
            return redirect('mapa')

        except Vaga.DoesNotExist:
            messages.error(request, 'Não foi encontrada nenhuma reserva ativa em seu nome para liberar.')
            return redirect('mapa')
        except Exception as e:
            print(f"---------------------------------------------------------")
            print(f"ERRO DETALHADO EM sair_da_vaga:")
            print(f"Tipo do Erro: {type(e).__name__}")
            print(f"Mensagem do Erro: {str(e)}")
            print(f"Traceback Completo:")
            traceback.print_exc() 
            print(f"---------------------------------------------------------")
            
            messages.error(request, f'Ocorreu um erro ao tentar sair da vaga. Por favor, tente novamente.')
            return redirect('mapa')
    
    return redirect('mapa')


def politica_privacidade(request):
    return render(request,'politica_privacidade.html')

def termos_de_uso(request):
    return render(request,'termos_de_uso.html')

def suporte(request):
    return render(request,'suporte.html')

@login_required 
def favoritos(request):
    return render(request,'favoritos.html')
