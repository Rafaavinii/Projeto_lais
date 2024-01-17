from typing import Any
from django.core.management.base import BaseCommand
from projeto_lais.consumirXML import XMLparser
from estabelecimento.models import Estabalecimento

class Command(BaseCommand):
    help = 'Insere estabelecimentos de saúde a partir de um arquivo XML'

    def handle(self, *args, **options):
        url = 'https://selecoes.lais.huol.ufrn.br/media/estabelecimentos_pr.xml'
        estabelecimentos = XMLparser(url, 'estabelecimento', ['no_fantasia', 'co_cnes'])

        for estabelecimento in estabelecimentos:
            nome = estabelecimento['no_fantasia']
            codigo= estabelecimento['co_cnes']
            try:
                Estabalecimento.objects.create(
                    nome=nome,
                    codigo=codigo,
                )
                self.stdout.write(self.style.SUCCESS(f'Sucesso ao inserir {nome}'))
            except Exception as e:
                print(f'Estabelecimento já adicionado \n{e}')
