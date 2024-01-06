from django.shortcuts import redirect, render
from .models import Agendamento
from candidato.models import Candidato
from estabelecimento.models import Estabalecimento
from django.contrib import messages
import xml.etree.ElementTree as ET
from .utils import *
from estabelecimento.utils import obter_estabelecimentos
from candidato.utils import obter_dados_usuario
from projeto_lais.validators import *

def agendamento_view(request):
    if request.method == 'GET':
        usuario = request.user
        estabelecimentos = obter_estabelecimentos()
        dados_usuario = obter_dados_usuario(usuario)
        idade = dados_usuario['idade']


        datas = disponibilidade_estabelecimento(Estabalecimento.objects.get(id=1))
        
        hora = horario_por_idade(idade)
    
        return render(request, 'form_agendamento.html', {
            'estabelecimentos': estabelecimentos, 
            'dados_usuario': dados_usuario, 
            'hora': hora,
            'datas': datas
        })
      
    if request.method == 'POST':

        usuario = request.user

        estabelecimento = request.POST.get('estabelecimento')
        cod, no_estabelecimento = estabelecimento.split(',')
        horario = request.POST.get('hora')
        hora, minuto = horario.split(':')


        data = '2024-01-10'
        jah_expirou = False
        candidato = Candidato.objects.get(id=usuario.id)
        estabelecimento = Estabalecimento.objects.get(codigo=cod)

        if agendamento_por_vez(usuario) and validar_data_agendamento(data):
            Agendamento.objects.create(
                data = data,
                hora = hora,
                minuto = minuto,
                dia = 'quarta',
                jah_expirou = jah_expirou,
                candidato = candidato,
                estabelecimento = estabelecimento
            )
            return redirect('pagina_inicial')
        
        elif not agendamento_por_vez(usuario):
            messages.error(request, 'Você já possui agendamento.')
        
        elif not validar_data_agendamento(data):
            messages.error(request, 'Data ou dia da semana inválido. Por favor, escolha uma dia entre quarta-feira e sábado.')

        return redirect('pagina_inicial')




