from datetime import datetime
from agendamento.models import Agendamento
from estabelecimento.models import Estabalecimento
from projeto_lais.consumirXML import XMLparser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def obter_grupos():
    xml_url = 'https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml'

    grupos = XMLparser(xml_url, 'grupoatendimento', ['codigo_si_pni', 'nome'])

    return grupos

def obter_dados_usuario(usuario):
    data_nascimento = usuario.data_nascimento
    idade = calcular_idade(data_nascimento)
    apto = verificar_apto(usuario.teve_covid, data_nascimento, usuario.grupo_atendimento)

    return {
        'nome': usuario.nome_completo,
        'data_nascimento': data_nascimento,
        'idade': idade,
        'cpf': usuario.cpf,
        'apto': apto,
    }

def calcular_idade(data_nascimento):
    data_atual = datetime.now()
    
    return data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))


def verificar_apto(teve_covid, data_nascimento, grupo_atendimento):
    if type(data_nascimento) == str:
        data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
    
    grupo_nao_apto = ['População Privada de Liberdade', 'Pessoas com Deficiência Institucionalizadas', 'Pessoas ACAMADAS de 80 anos ou mais']
    
    if teve_covid or calcular_idade(data_nascimento) < 18 or grupo_atendimento in grupo_nao_apto:
        apto = False
    else:
        apto = True
    
    return apto

def obter_agendamentos_pagina(request, usuario, ordem='decrescente'):
    #filtrando agendamentos por usuario
    agendamentos = Agendamento.objects.filter(candidato_id=usuario.id)
    

    #Verificando se o agendamento já expirou
    for agendamento in agendamentos:
        if str(agendamento.data) < str(datetime.now().date()):
            agendamento.jah_expirou = True
            agendamento.save()
        
        elif str(agendamento.data) == str(datetime.now().date()) and str(agendamento.hora) <= str(datetime.now().hour):
            agendamento.jah_expirou = True
            agendamento.save()

    #orgenando por data e hora
    if ordem == 'crescente':
        agendamentos = agendamentos.order_by('data', 'hora')
    else:
        agendamentos = agendamentos.order_by('-data', '-hora')

    lista_agendamento = []
    for agendamento in agendamentos:
        estabelecimento = Estabalecimento.objects.get(id=agendamento.estabelecimento.id)
        agendamento.__dict__.update({'nome_estabelecimento': estabelecimento.nome, 'codigo_estabelecimento': estabelecimento.codigo})
        lista_agendamento.append(agendamento)
    

    # Número de agendamentos por página
    agendamentos_por_pagina = 6

    # Cria um objeto Paginator
    agendamentos_pagina = Paginator(lista_agendamento, agendamentos_por_pagina)

    # Obtém o número da página a partir dos parâmetros GET
    page_num = request.GET.get('page')
    agendamentos_pagina = agendamentos_pagina.get_page(page_num)

    return agendamentos_pagina