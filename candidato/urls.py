from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.candidato_view, name='candidato'),
    path('login/', views.login_candidato_view, name='login_candidato'),
    path('logout/', views.logout_view, name='logout'),
    path('pagina_inicial/', views.candidato_autenticado_view, name='pagina_inicial')
]