from django.shortcuts import redirect, render
from .models import Agendamento
from candidato.models import Candidato
from django.contrib import messages
import xml.etree.ElementTree as ET
from .utils import *
from projeto_lais.validators import *

def agendamento_view(request):  
    if request.method == 'POST':

        usuario = request.user.id 

        estabelecimento = request.POST.get('estabelecimento')
        cod, no_estabelecimento = estabelecimento.split(',')

        data = request.POST.get('data')
        hora = request.POST.get('hora')
        dia = dia_da_semana(data)
        jah_expirou = False
        codigo_estabelecimento = cod
        nome_estabelecimento = no_estabelecimento
        candidato = Candidato.objects.get(id=usuario)

        if not validar_data_agendamento(data):
            msg_erro = "Data inserida inválida. Por favor, tente novamente."
            messages.error(request, msg_erro)
            return redirect('pagina_inicial')

        Agendamento.objects.create(
            data = data,
            hora = hora,
            dia = dia,
            jah_expirou = jah_expirou,
            codigo_estabelecimento = codigo_estabelecimento,
            nome_estabelecimento = nome_estabelecimento,
            candidato = candidato
        )

        return redirect('pagina_inicial')





