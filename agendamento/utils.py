from datetime import datetime


def dia_da_semana(data):
    data_formatada = datetime.strptime(data, '%Y-%m-%d')
    dia_da_semana = data_formatada.weekday()
    nomes_dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    nome_dia_da_semana = nomes_dias_semana[dia_da_semana]
    return nome_dia_da_semana