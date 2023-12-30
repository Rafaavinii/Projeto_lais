from datetime import datetime
from django.shortcuts import redirect, render
from .models import Agendamento
from candidato.models import Candidato

def agendamento(request):
    hoje = datetime.now()
    data = hoje.date()
    hora = f'{hoje.hour}:{hoje.minute}'
    dia = hoje.day
    jah_expirou = False
    codigo_estabelecimento = '3355926'
    nome_estabelecimento = 'PRO ANALISES SERVICOS DE ANALISES CLINICAS LTDA'
    candidato = Candidato.objects.get(id=3)

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
