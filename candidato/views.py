from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import xml.etree.ElementTree as ET
import requests
from .models import Candidato
from agendamento.models import Agendamento

def candidato(request):
    if request.method == 'GET':

        # Enviando o grupos para o select
        xml_url = 'https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml'

        response = requests.get(xml_url)

        if response.status_code == 200:
            root = ET.fromstring(response.content)

            grupos = []
            for grupo in root.findall('grupoatendimento'):
                codigo = grupo.find('nome').text
                nome = grupo.find('nome').text
                grupos.append({'codigo': codigo, 'nome': nome})

            context = {'grupos': grupos}

        return render(request, 'candidato.html', context)
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        grupo_atendimento = request.POST.get('grupoAtendimento')
        teve_covid = request.POST.get('teve_covid')
        senha = request.POST.get('senha')
        
        if teve_covid == "nao":
            teve_covid = False
        else:
            teve_covid = True

        candidato = Candidato.objects.create_user(
            nome_completo = nome,
            username=cpf,
            cpf=cpf,
            data_nascimento=data_nascimento,
            grupo_atendimento=grupo_atendimento,
            teve_covid=teve_covid,
            password=senha
        )

        candidato.save()

        messages.success(request, 'Cadastro realizado com sucesso. Faça login para continuar.')

        return redirect('login_candidato')

def login_candidato(request):
    if request.method == "GET":
        return render(request, 'login_candidato.html')

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
def candidato_autenticado(request):
    if request.method == "GET":

        usuario = request.user

        nome = usuario.nome_completo
        data_nascimento = usuario.data_nascimento
        cpf = usuario.cpf
        teve_covid = usuario.teve_covid
        grupo_atendimento = usuario.grupo_atendimento

        # calcular idade
        data_atual = datetime.now()
        idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))

        #apto?
        grupo_nao_apto = ['População Privada de Liberdade', 'Pessoas com Deficiência Institucionalizadas', 'Pessoas ACAMADAS de 80 anos ou mais']
        if teve_covid or idade < 18 or grupo_atendimento in grupo_nao_apto:
            apto = 'Não'
        else:
            apto = 'Sim'
        
        #filtrando agendamentos por usuario
        agendamentos = Agendamento.objects.filter(candidato_id=usuario.id)

        lista_agendamento = []
        for agendamento in agendamentos:
            lista_agendamento.append(agendamento.__dict__)
        
        # Número de agendamentos por página
        agendamentos_por_pagina = 6

        # Cria um objeto Paginator
        agendamentos_pagina = Paginator(lista_agendamento, agendamentos_por_pagina)

        # Obtém o número da página a partir dos parâmetros GET
        page_num = request.GET.get('page')
        agendamentos_pagina = agendamentos_pagina.get_page(page_num)
        
        context = {
            'dados_usuario': {
                'nome': nome,
                'data_nascimento': data_nascimento,
                'idade': idade,
                'cpf': cpf,
                'apto': apto,
            },
            'agendamentos_pagina': agendamentos_pagina,
        }


        return render(request, 'pagina_inicial.html', context)