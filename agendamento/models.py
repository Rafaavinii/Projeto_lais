from django.db import models
from candidato.models import Candidato

class Agendamento(models.Model):
    data = models.DateField()
    hora = models.CharField(max_length=5)
    dia = models.CharField(max_length=10)
    jah_expirou = models.BooleanField()
    codigo_estabelecimento = models.CharField(max_length=7)
    nome_estabelecimento = models.CharField(max_length=150)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.candidato) + str(self.data)