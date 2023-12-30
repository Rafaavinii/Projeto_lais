from datetime import datetime
from django.shortcuts import redirect, render
from .models import Agendamento
from candidato.models import Candidato
import xml.etree.ElementTree as ET
import requests

def agendamento(request):

    
    if request.method == 'POST':

        usuario = request.user.id

        data = request.POST.get('data')
        hora = request.POST.get('hora')
        dia = request.POST.get('dia')
        jah_expirou = False
        codigo_estabelecimento = request.POST.get('estabelecimento')
        nome_estabelecimento = request.POST.get('estabelecimento')
        candidato = Candidato.objects.get(id=usuario)

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
