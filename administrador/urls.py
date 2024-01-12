from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_administrador_view, name='login_administrador'),
    path('dashboard/', views.administrador_dashboard_view, name='administrador_dashboard'),
    path('gerenciamento/', views.administrador_estabelecimento_view, name='administrador_estabelecimento'),
    path('buscar_estabelecimento/', views.buscar_estabelecimento, name='buscar_estabelecimento'),
]