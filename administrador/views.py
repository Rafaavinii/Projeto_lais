from random import randint
from django.shortcuts import render

from projeto_lais.consumirXML import XMLparser

def administrador_dashboard_view(request):
    estabelecimentos = obter_estabelecimentos()
    nomes = [estabelecimento['no_fantasia'] for estabelecimento in estabelecimentos]
    quantidades = [randint(10, 100) for estabelecimento in estabelecimentos]
    bar_data = {'label': nomes, 'quantidade': quantidades}
    return render(request, 'dashboard_adiministracao.html', bar_data)

def obter_estabelecimentos():
    xml_url = 'https://selecoes.lais.huol.ufrn.br/media/estabelecimentos_pr.xml'
    return XMLparser(xml_url, 'estabelecimento', ['no_fantasia', 'co_cnes'])