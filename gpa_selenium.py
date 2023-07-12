from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv


load_dotenv()
IDUFF = "https://app.uff.br/iduff/"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")


servico =  Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service = servico, options=chrome_options)

browser.get(IDUFF)


login = browser.find_element(By.XPATH,'//*[@id="login:id"]').send_keys(os.getenv('LOGIN'))
print('inserindo login...')
senha= browser.find_element(By.XPATH,'//*[@id="login:senha"]').send_keys(os.getenv('SENHA'))
print('inserindo senha...')
logar = browser.find_element(By.XPATH,'//*[@id="login:btnLogar"]').click()
print('logando...')
try:
     
    perfis = WebDriverWait(browser, 1).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="templatePrincipal2:j_id203_body"]/h3'))
    )
    seleciona_perfil = browser.find_elements('xpath', '//*[@id="menurecursos"]/li/a')
    ultimo_perfil = seleciona_perfil[-1]
    ultimo_perfil.click()
except:
     pass
try:
     
     pop_up = WebDriverWait(browser, 1).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/img'))
    )
     browser.find_element('xpath','/html/body/div[3]/div[2]/div/div[2]/div/img').click()
except:
    pass


historico = browser.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[1]/div[3]/form/div[3]/div/ul[3]/li/a').click()
print("buscando historico...")

tabela = browser.find_element(By.ID,'historico:tblDisciplinasHistorico')

corpo_tabela = tabela.find_element(By.TAG_NAME,"tbody")
linhas = corpo_tabela.find_elements(By.TAG_NAME,"tr")

materias = {}
def coleta_disciplinas(materias, linhas):
    for linha in linhas:
        coluna = linha.find_elements(By.TAG_NAME, "td")
        if len(coluna[4].text) == 0:
            continue
        
        nota = float(coluna[4].text)
        nome  = coluna[1].text.lower()
        carga_horaria = int(coluna[7].text)
        materias[nome] = [nota, carga_horaria]
        

def calculo_cr(materias):
    ch_total = 0
    cr_total = 0
    for disciplina in materias:
        nota, carga_horaria = materias[disciplina]
        cr_total += nota*carga_horaria
        ch_total += carga_horaria


    return round((cr_total/ch_total),1)
print("calculando cr...")
coleta_disciplinas (materias, linhas)
cr = calculo_cr(materias)

print(f"seu CR e: {cr}")