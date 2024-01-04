from django.urls import path
from . import views

urlpatterns = [
    path('', views.administrador_dashboard_view, name='administrador_dashboard'),
]