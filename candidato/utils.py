from datetime import datetime
from agendamento.models import Agendamento
from projeto_lais.consumirXML import XMLparser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def obter_grupos():
    xml_url = 'https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml'

    grupos = XMLparser(xml_url, 'grupoatendimento', ['codigo_si_pni', 'nome'])

    return grupos

def obter_dados_usuario(usuario):
    data_nascimento = usuario.data_nascimento
    idade = calcular_idade(data_nascimento)
    apto = verificar_apto(usuario)

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


def verificar_apto(usuario):
    grupo_nao_apto = ['População Privada de Liberdade', 'Pessoas com Deficiência Institucionalizadas', 'Pessoas ACAMADAS de 80 anos ou mais']
    if usuario.teve_covid or calcular_idade(usuario.data_nascimento) < 18 or usuario.grupo_atendimento in grupo_nao_apto:
        apto = 'Não'
    else:
        apto = 'Sim'
    
    return apto


def obter_estabelecimentos():
    xml_url = 'https://selecoes.lais.huol.ufrn.br/media/estabelecimentos_pr.xml'
    return XMLparser(xml_url, 'estabelecimento', ['no_fantasia', 'co_cnes'])


def obter_agendamentos_pagina(request, usuario):
    #filtrando agendamentos por usuario
    agendamentos = Agendamento.objects.filter(candidato_id=usuario.id)

    lista_agendamento = []
    for agendamento in agendamentos:
        lista_agendamento.append(agendamento.__dict__)
    
    # Número de agendamentos por página
    agendamentos_por_pagina = 6

    # Cria um objeto Paginator
    agendamentos_pagina = Paginator(lista_agendamento, agendamentos_por_pagina)

    # Obtém o número da página a partir dos parâmetros GET
    page_num = request.GET.get('page')
    agendamentos_pagina = agendamentos_pagina.get_page(page_num)

    return agendamentos_pagina