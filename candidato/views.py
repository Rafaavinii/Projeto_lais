from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import xml.etree.ElementTree as ET
import requests
from .models import Candidato

def candidato(request):
    if request.method == 'GET':
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

        return redirect('login_candidato.html')

def login_candidato(request):
    if request.method == "GET":
        return render(request, 'login_candidato.html')

    if request.method == "POST":
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        candidato = authenticate(request, cpf=cpf, password=senha)
        
        if candidato is not None:
            login(request, candidato)
            return redirect('pagina_inicial')
        else:
            messages.error(request, 'CPF ou senha incorretos.')
            return render(request, 'login_candidato.html')

def logout_view(request):
    logout(request)
    return redirect('pagina_inicial')

@login_required
def candidato_autenticado(request):
    if request.method == "GET":

        nome = request.user.nome_completo
        data_nascimento = request.user.data_nascimento
        cpf = request.user.cpf

        context = {
            'nome': nome,
            'data_nascimento': data_nascimento,
            'cpf': cpf
        }

        return render(request, 'pagina_inicial.html', context)