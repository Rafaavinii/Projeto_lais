from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.administrador_dashboard_view, name='administrador_dashboard'),
    path('gerenciamento/', views.administrador_estabelecimento_view, name='administrador_estabelecimento'),
]