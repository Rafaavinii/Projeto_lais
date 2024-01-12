from random import randint
import csv

from projeto_lais.consumirXML import XMLparser

def ler_csv(nome_arquivo):
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        lista = []
        for linha in leitor_csv:
            lista.append(linha[0])
        
        return lista
    
def gerar_data():
    ano = randint(1950, 2005)
    mes = randint(1, 12)
    if mes >= 1 and mes < 10:
        mes = f'0{mes}'
    dia = randint(1, 31)
    return f"{ano}-{mes}-{dia}"

def obter_grupos():
    xml_url = 'https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml'

    grupos = XMLparser(xml_url, 'grupoatendimento', ['codigo_si_pni', 'nome'])

    return grupos[randint(0, len(grupos))]['nome']


def gerar_candidato():
    candidatos = []
    cpfs = ler_csv('cpfs_list.csv')
    boolean = [False, True]

    for i in range(29):
        candidatos.append({
            "nome": f"CANDIDATO {i}",
            "cpf": cpfs[i],
            "data_nascimento": gerar_data(),
            "grupo_atendimento": obter_grupos(),
            "teve_covid": boolean[randint(0, 1)],
            "senha": "Abcd1234"
        })
        print(f'Gerando candidatos... {round((i/10)*29, 2 )}%', end="\r")
    
    return candidatos


dic = {}

for i in range(10):
    dic[f'{i}'] = []

print(dic)
        