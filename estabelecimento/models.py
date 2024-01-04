from django.db import models
from agendamento.models import Agendamento

class Estabalecimento(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=8, unique=True)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome