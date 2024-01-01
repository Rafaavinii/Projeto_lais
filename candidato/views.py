from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from projeto_lais.validators import *
from .utils import *
from .models import Candidato

def candidato_view(request):
    if request.method == 'GET':
        context = {"grupos": obter_grupos()}
        return render(request, 'candidato.html', context)
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        grupo_atendimento = request.POST.get('grupoAtendimento')
        teve_covid = request.POST.get('teve_covid')
        senha = request.POST.get('senha')
        confirmarSenha = request.POST.get('confirmarSenha')
        
        if teve_covid == "nao":
            teve_covid = False
        else:
            teve_covid = True

        if validar_cadastro(cpf, data_nascimento, senha, confirmarSenha)[0]:
            #Mostrar mensagens de erros e campos
            mensagens_erro = validar_cadastro(cpf, data_nascimento, senha, confirmarSenha)[0]
            campos_erro = validar_cadastro(cpf, data_nascimento, senha, confirmarSenha)[1]
            context = {
                'grupos': obter_grupos(),
                'mensagens_erro': mensagens_erro,
                'campos_erro': campos_erro,
                'campos_data': { 
                    "nome": nome, 
                    "cpf": cpf,
                    "data_nascimento":  data_nascimento,
                    "grupo_atendimento": grupo_atendimento, 
                    "teve_covid": teve_covid,
                }
            }
            return render(request, 'candidato.html', context)

        print(verificar_apto(teve_covid, data_nascimento, grupo_atendimento))
        if verificar_apto(teve_covid, data_nascimento, grupo_atendimento):
            #salvando candidato no banco
            Candidato.objects.create_user(
                nome_completo = nome,
                username=cpf,
                cpf=cpf,
                data_nascimento=data_nascimento,
                grupo_atendimento=grupo_atendimento,
                teve_covid=teve_covid,
                password=senha
            )
            messages.success(request, 'Candidato cadastrado com sucesso!')
            return redirect('login_candidato')
        
        else:
            messages.error(request, 'Você não é apto para participar da pesquisa!')
            return redirect('candidato')

def login_candidato_view(request):
    if request.method == "GET":
        sucesso_message = messages.get_messages(request)
        return render(request, 'login_candidato.html', {'mensagem_sucesso': sucesso_message})

    if request.method == "POST":
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        #autenticando candidato
        candidato = authenticate(request, cpf=cpf, password=senha)
        
        if candidato is not None:
            login(request, candidato)
            return redirect('pagina_inicial')
        else:
            messages.error(request, 'CPF ou senha incorretos.')
            return render(request, 'login_candidato.html')

def logout_view(request):
    # logout do candidato
    logout(request)
    return redirect('pagina_inicial')

@login_required
def candidato_autenticado_view(request):
    if request.method == "GET":
        usuario = request.user
        dados_usuario = obter_dados_usuario(usuario)
        agendamentos_pagina = obter_agendamentos_pagina(request, usuario)
        estabelecimentos = obter_estabelecimentos()
        
        context = {
            'dados_usuario': dados_usuario,
            'agendamentos_pagina': agendamentos_pagina,
            'estabelecimentos': estabelecimentos,
        }

        return render(request, 'pagina_inicial.html', context)