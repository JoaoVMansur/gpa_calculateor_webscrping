import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os 



load_dotenv()

secao = requests.Session()
response = secao.get("https://app.uff.br/iduff/")

biscoito = secao.cookies.get("JSESSIONID")
data = {
    'login': 'login',
    'login:id':os.getenv("LOGIN"),
    'login:senha': os.getenv("SENHA"),
    'login:btnLogar': 'Logar',
    'javax.faces.ViewState': 'j_id1',
}

login = secao.post(f'https://app.uff.br/iduff/login.uff;jsessionid={biscoito}',data=data,)

params = {
    'conversationPropagation': 'none',
}

historico = secao.get('https://app.uff.br/iduff/privado/declaracoes/private/historico.uff', params=params,)

soup = BeautifulSoup(historico.text.encode('utf-8'), "html.parser")

tabela = soup.find_all('table', attrs={'id':'historico:tblDisciplinasHistorico'})
corpo_tabela = tabela[0].find("tbody")
linhas = corpo_tabela.find_all("tr")
materias = {}


for linha in linhas:
    coluna = linha.find_all("td")
    if len(coluna[4].contents) == 0:
        continue
    
    nota = float(coluna[4].contents[0])
    nome  = coluna[1].contents[0].lower()
    carga_horaria = int(coluna[7].contents[0])
    materias[nome] = [nota, carga_horaria]

def calculo_cr(materias):
    ch_total = 0
    cr_total = 0
    for disciplina in materias:
        nota, carga_horaria = materias[disciplina]
        cr_total += nota*carga_horaria
        ch_total += carga_horaria


    return round((cr_total/ch_total),1)


cr = calculo_cr(materias)

print(cr)
