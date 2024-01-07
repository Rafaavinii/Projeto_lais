from django.urls import path
from . import views

app_name = 'agendamento'

urlpatterns = [
    path('', views.agendamento_view, name='agendamento'),
    path('obter-datas-disponiveis/<int:estabelecimento>/', views.obter_datas_disponiveis_view, name='obter-datas-disponiveis'),
    path('obter-minutos-disponiveis/<int:estabelecimento>/<str:data>/<str:hora>/', views.obter_minutos_disponiveis_view, name='obter_minutos_disponiveis')
]