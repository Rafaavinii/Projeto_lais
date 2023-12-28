from django.db import models
from django.contrib.auth.models import AbstractUser

class Candidato(AbstractUser):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    grupo_atendimento = models.CharField(max_length=255, blank=True, null=True)
    teve_covid = models.BooleanField(default=False)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome_completo', 'data_nascimento']

    def __str__(self):
        return self.nome_completo

