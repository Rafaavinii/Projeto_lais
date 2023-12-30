from django.urls import path
from . import views

app_name = 'agendamento'

urlpatterns = [
    path('', views.agendamento, name='agendamento'),
]