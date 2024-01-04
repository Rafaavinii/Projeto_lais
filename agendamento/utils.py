from datetime import datetime

from agendamento.models import Agendamento


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