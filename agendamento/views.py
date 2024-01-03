from django.shortcuts import redirect, render
from .models import Agendamento
from candidato.models import Candidato
from django.contrib import messages
import xml.etree.ElementTree as ET
from .utils import *
from projeto_lais.validators import *

def agendamento_view(request):  
    if request.method == 'POST':

        usuario = request.user

        estabelecimento = request.POST.get('estabelecimento')
        cod, no_estabelecimento = estabelecimento.split(',')

        data = request.POST.get('data')
        hora = request.POST.get('hora')
        dia = dia_da_semana(data)
        jah_expirou = False
        codigo_estabelecimento = cod
        nome_estabelecimento = no_estabelecimento
        candidato = Candidato.objects.get(id=usuario.id)

        # if agendamento_por_vez(usuario) and validar_data_agendamento(data):
        if True:
            Agendamento.objects.create(
                data = data,
                hora = hora,
                dia = dia,
                jah_expirou = jah_expirou,
                codigo_estabelecimento = codigo_estabelecimento,
                nome_estabelecimento = nome_estabelecimento,
                candidato = candidato
            )
        elif not agendamento_por_vez(usuario):
            messages.error(request, 'Você já possui agendamento.')
        
        elif not validar_data_agendamento(data):
            messages.error(request, 'Fata inválida.')

        return redirect('pagina_inicial')

def agendamento_por_vez(usuario):
    agendamento = Agendamento.objects.filter(candidato_id=usuario.id).last()
    if not agendamento or agendamento.jah_expirou == True:
        return True
    
    return False




