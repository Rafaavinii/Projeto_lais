from datetime import datetime

from agendamento.models import Agendamento
from django.db.models import Count


def dia_da_semana(data):
    data_formatada = datetime.strptime(data, '%Y-%m-%d')
    dia_da_semana = data_formatada.weekday()
    nomes_dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    nome_dia_da_semana = nomes_dias_semana[dia_da_semana]
    return nome_dia_da_semana

def agendamento_por_vez(usuario):
    agendamento = Agendamento.objects.filter(candidato_id=usuario.id).last()
    if not agendamento or agendamento.jah_expirou == True:
        return True
    
    return False

# def vagas_estabelecimento(estabelecimento):
#     agendamentos = Agendamento.objects.filter(estabelecimento_id=estabelecimento.id)

#     for agendamento in agendamentos:
#         agendamento
    
#     if cont >= 5:
#         return False
    
#     return True

def disponibilidade_estabelecimento(estabelecimento):
    estabelecimentos = Agendamento.objects.filter(estabelecimento_id=estabelecimento)
    datas_iguais = estabelecimentos.values('data', 'hora').annotate(total=Count('data'))
    indisponiveis = {'data': [], 'hora':[]}

    for agendamento in datas_iguais:
        if agendamento['total'] >= 5:
            indisponiveis['data'].append(agendamento['data'])
            indisponiveis['hora'].append(agendamento['hora'])


    
    print(indisponiveis)
    
    
    return True