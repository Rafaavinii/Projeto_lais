from django.shortcuts import render

def administrador_view(request):
    return render(request, 'base_painel_adm.html')
