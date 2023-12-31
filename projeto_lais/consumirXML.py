import xml.etree.ElementTree as ET
import requests

def XMLparser(url, topo, chaves):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            lista = []
            dicionario_temp = {}
            for temp in root.findall(topo):
                for chave in chaves: 
                    valor = temp.find(chave).text
                    dicionario_temp[chave] = valor
                lista.append(dicionario_temp)
                dicionario_temp = {}

            return lista
        
    except requests.RequestException as e:
        print(f'Erro na requisição: {e}')
        return 'error'