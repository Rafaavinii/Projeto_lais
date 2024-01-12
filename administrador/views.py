from random import randint
from django.shortcuts import render, redirect
from agendamento.models import Agendamento
from candidato.models import Candidato
from candidato.utils import verificar_apto
from estabelecimento.models import Estabalecimento
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

from projeto_lais.consumirXML import XMLparser

def login_administrador_view(request):
    if request.method == 'GET':
        return render(request, 'login_adm.html')
    
    if request.method == "POST":
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        #autenticando candidato
        candidato = authenticate(request, username=cpf, password=senha)
        if candidato is not None:
            adm = Candidato.objects.get(nome_completo=candidato)
            if adm.is_superuser:
                login(request, candidato)
                return redirect('administrador_dashboard')
        
            elif not adm.is_superuser:
                messages.error(request, 'Você não tem permissão.')
                return redirect('login_candidato')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return render(request, 'login_adm.html')

@permission_required('is_superuser')
def administrador_dashboard_view(request):
    estabelecimentos = Estabalecimento.objects.all()

    dados_barra = {'nomes': [], 'quantidade': []}
    dados_pizza = {'aptos': 0, 'inaptos': 0}   

    for estabelecimento in estabelecimentos:
        dados_barra['nomes'].append(estabelecimento.nome)
        dados_barra['quantidade'].append(len(Agendamento.objects.filter(estabelecimento=estabelecimento)))

    candidatos = Candidato.objects.all()

    for candidato in candidatos:
        if verificar_apto(candidato.teve_covid, candidato.data_nascimento, candidato.grupo_atendimento):
            dados_pizza['aptos'] += 1 
        else:
            dados_pizza['inaptos'] += 1
    

    dados_grafico = {'barra': dados_barra, 'pizza': dados_pizza}
    return render(request, 'dashboard_adiministracao.html', dados_grafico)

@permission_required('is_superuser')
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

def buscar_estabelecimento(request):
    if 'term' in request.GET:
        term = request.GET['term']
        estabelecimentos = Estabalecimento.objects.filter(Q(nome__icontains=term) | Q(codigo__icontains=term))
        lista_estabelecimente = [{'nome': estabalecimento.nome, 'codigo': estabalecimento.codigo} for estabalecimento in estabelecimentos]
        return JsonResponse({'estabelecimentos': lista_estabelecimente})
    return JsonResponse({})