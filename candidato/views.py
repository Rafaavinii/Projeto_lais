from django.shortcuts import render
from django.http import HttpResponse
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

        candidato = Candidato(
            nome_completo = nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            grupo_atendimento=grupo_atendimento,
            teve_covid=teve_covid,
            password=senha
        )

        candidato.save()

        return HttpResponse('CADASTRADO COM SUCESSO!')

