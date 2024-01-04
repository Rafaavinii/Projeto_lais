from typing import Any
from django.core.management.base import BaseCommand
from candidato.utils import obter_estabelecimentos
from estabelecimento.models import Estabalecimento

class Command(BaseCommand):
    help = 'Insere estabelecimentos de saúde a partir de um arquivo XML'

    def handle(self, *args, **options):
        estabelecimentos = obter_estabelecimentos()

        for estabelecimento in estabelecimentos:
            nome = estabelecimento['no_fantasia']
            codigo= estabelecimento['co_cnes']
            Estabalecimento.objects.create(
                nome=nome,
                codigo=codigo,
            )
            self.stdout.write(self.style.SUCCESS(f'Sucesso ao inserir {nome}'))
