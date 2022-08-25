import requests as re
from bs4 import BeautifulSoup

def retorna_lista_datas():
    url = 'http://www.unirio.br/prograd/calendario-academico'
    r = re.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tabela = soup.findAll('table')[1] # segunda tabela é sobre o segundo período
    dados = tabela.findAll('td') # todas as entradas de dados da tabela
    resultado = [] # lista de strings das linhas da tabela
    for i in range(0, len(dados), 2):
        resultado.append((dados[i].text + ': ' + dados[i + 1].text.strip()).strip())
    # cada elemento da lista é uma linha da tabela
    return resultado

datas = retorna_lista_datas()

for data in datas:
    print(data)
