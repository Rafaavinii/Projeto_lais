from datetime import datetime
import calendar
from agendamento.models import Agendamento
from django.db.models import Count

def agendamento_por_vez(usuario):
    agendamento = Agendamento.objects.filter(candidato_id=usuario.id).last()
    if not agendamento or agendamento.jah_expirou == True:
        return True
    
    return False

def disponibilidade_estabelecimento(estabelecimento):
    estabelecimentos = Agendamento.objects.filter(estabelecimento_id=estabelecimento)
    datas_iguais = estabelecimentos.values('data', 'hora').annotate(total=Count('data'))
    indisponiveis = {'data': [], 'hora':[]}

    for agendamento in datas_iguais:
        if agendamento['total'] >= 5:
            indisponiveis['hora'].append(agendamento['hora'])
    
    indisponiveis['data'].append(agendamento['data'])

    datas = obter_dias_quarta_a_sabado(2024, 1)
    
    for data in indisponiveis['data']:
        data = str(data)
        if data in datas:
            datas.remove(data)

    return datas

def obter_dia_da_semana(data):
    data_formatada = datetime.strptime(data, '%Y-%m-%d')
    dia_da_semana = data_formatada.weekday()
    return dia_da_semana

def obter_dias_quarta_a_sabado(ano, mes):
    # Retorna uma matriz de listas onde cada lista representa uma semana do mês
    semanas = calendar.monthcalendar(ano, mes)
    datas = []
    # Itera sobre cada semana do mês
    for semana in semanas:
        # Itera sobre cada dia da semana
        for dia in semana:
            # Se o dia estiver dentro do mês, imprima a data
            if dia != 0:
                data = f'{ano}-{mes:02d}-{dia:02d}'
                if not obter_dia_da_semana(data) in [0, 1, 6]:
                    datas.append(data)
    
    return datas