from datetime import datetime
import re
from candidato.models import Candidato

def validar_senha(senha):
    # Comprimento mínimo de 8 caracteres
    mensagens_erro = []
    if len(senha) < 8:
        mensagens_erro.append('A senha deve ter pelo menos 8 caracteres.')

    # Pelo menos uma letra maiúscula
    if not re.search(r'[A-Z]', senha):
        mensagens_erro.append('A senha deve conter pelo menos uma letra maiúscula.')

    # Pelo menos uma letra minúscula
    if not re.search(r'[a-z]', senha):
        mensagens_erro.append('A senha deve conter pelo menos uma letra minúscula.')

    # Pelo menos um número
    if not re.search(r'[0-9]', senha):
        mensagens_erro.append('A senha deve conter pelo menos um número.')

    return mensagens_erro

def validar_data(data):
    data_atual = datetime.now()
    if data >= str(data_atual):
        return False
    elif data < '1908-01-01':
        return False
    else:
        return True

def validar_cpf(cpf):
    #Deixa apenas números
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return 'CPF inválido.'
    
    if cpf == cpf[0] * 11:
        return 'CPF inválido.'
    
    #primeiro digito verificador
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10-i)
    resto = total % 11
    if resto > 1:
        primeiro_digito = 11 - resto
    else:
        primeiro_digito = 0 
    
    if primeiro_digito != int(cpf[9]):
        return 'CPF inválido.'
    
    #segundo digito verificador
    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11-i)
    resto = total % 11
    if resto > 1:
        segundo_digito = 11 - resto
    else:
        segundo_digito = 0 

    if primeiro_digito != int(cpf[9]):
        return 'CPF inválido.'
    
    if Candidato.objects.filter(cpf=cpf).exists():
        return 'CPF já cadastrado.'

def validar_data_agendamento(data):
    data_formatada = datetime.strptime(data, '%Y-%m-%d')
    dia_da_semana = data_formatada.weekday()
    data_atual = datetime.now()
    if data < str(data_atual) or (dia_da_semana in [0, 1, 6]):
        return False
    return True

def validar_cadastro(cpf, data, senha, confirm_senha):
    mensagens_erro = []
    campo_erro = []
    if validar_cpf(cpf):
        mensagens_erro.append(validar_cpf(cpf))
        campo_erro.append('CPF')

    if not validar_data(data):
        mensagens_erro.append('Data de nascimento inválida!')
        campo_erro.append('data')

    if senha != confirm_senha:
        mensagens_erro.append('As senhas devem ser iguais.')
        campo_erro.append('ambas_senhas')

    if validar_senha(senha):
        campo_erro.append('senha')
        for msg in validar_senha(senha):
            mensagens_erro.append(msg)
    
    return (mensagens_erro, campo_erro)