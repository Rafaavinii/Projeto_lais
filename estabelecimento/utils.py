from estabelecimento.models import Estabalecimento


def obter_estabelecimentos():
    estabelecimentos = Estabalecimento.objects.all()
    lista_estabelecimento = []
    for estabalecimento in estabelecimentos:
        lista_estabelecimento.append(estabalecimento.__dict__)
    return lista_estabelecimento