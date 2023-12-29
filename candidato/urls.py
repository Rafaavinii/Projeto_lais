from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.candidato, name='candidato'),
    path('login/', views.login_candidato, name='login_candidato'),
    path('logout/', views.logout_view, name='logout'),
    path('pagina_inicial/', views.candidato_autenticado, name='pagina_inicial')
]