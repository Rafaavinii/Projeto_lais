from django.db import models

class Estabalecimento(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.nome