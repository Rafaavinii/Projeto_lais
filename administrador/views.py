from random import randint
from django.shortcuts import render
from candidato.models import Candidato
from candidato.utils import verificar_apto
from estabelecimento.models import Estabalecimento

from projeto_lais.consumirXML import XMLparser

def administrador_dashboard_view(request):
    estabelecimentos = obter_estabelecimentos()
    nomes = [estabelecimento['no_fantasia'] for estabelecimento in estabelecimentos]
    quantidades = [randint(10, 100) for estabelecimento in estabelecimentos]
    bar_data = {'label': nomes, 'quantidade': quantidades}

    candidatos = Candidato.objects.all()

    lista_aptos = []
    lista_inaptos = []
    for candidato in candidatos:
        if verificar_apto(candidato.teve_covid, candidato.data_nascimento, candidato.grupo_atendimento):
            lista_aptos.append(candidato)
        else:
            lista_inaptos.append(candidato)
    
    bar_data.update({"aptos": len(lista_aptos), "inaptos": len(lista_inaptos)})

    return render(request, 'dashboard_adiministracao.html', bar_data)

def administrador_estabelecimento_view(request):
    estabalecimentos = Estabalecimento.objects.all()
    filtro = request.GET.get('filtro')

    if filtro == 'codigo':
        estabalecimentos = estabalecimentos.order_by('codigo')

    lista_estabelecimento = []
    for estabalecimento in estabalecimentos:
        lista_estabelecimento.append(
            {
                'nome': estabalecimento.nome,
                'codigo': estabalecimento.codigo
            }
        )
    
    context = {'estabelecimentos': lista_estabelecimento, 'filtro': filtro}

    return render(request, 'estabelecimento_administracao.html', context)

def obter_estabelecimentos():
    xml_url = 'https://selecoes.lais.huol.ufrn.br/media/estabelecimentos_pr.xml'
    return XMLparser(xml_url, 'estabelecimento', ['no_fantasia', 'co_cnes'])