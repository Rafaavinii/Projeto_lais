from django.urls import path
from . import views

urlpatterns = [
    path('', views.administrador_view, name='administrador'),
]