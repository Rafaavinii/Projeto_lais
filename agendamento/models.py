from django.db import models
from candidato.models import Candidato
from estabelecimento.models import Estabalecimento

class Agendamento(models.Model):
    data = models.DateField()
    hora = models.CharField(max_length=5)
    minuto = models.CharField(max_length=2)
    dia = models.CharField(max_length=10)
    jah_expirou = models.BooleanField()
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabalecimento, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.candidato) + str(self.data) + str(self.estabelecimento)