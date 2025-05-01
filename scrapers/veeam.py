from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os # serve para trabalhar como arquivos/pasta de maquina
import pandas as pd #trabalhar com o excel 
from datetime import datetime, date
import time 

ULTIMA_CONSULTA = datetime(2025, 4, 10, 12, 0, 0)  # ano, mês, dia, hora, minuto, segundo TESTES
hoje = '09-04-2025'
ontem = '08-04-2025'

USER = os.getenv("USERNAME")
RELATORIO = rf"C:\Users\{USER}\Desktop\Relatorio.xlsx"


def acessarSite():
    options = Options()
    options.add_argument("--start-maximized") 
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://www.veeam.com/kb"
    ]

    for pagina in paginas:
        nav.get(pagina)
        """
        try:
            close_banner = WebDriverWait(nav, 25).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'dismiss-button'))
            )

            close_banner[0].click()
        except (TimeoutException) as e:
               print("Erro ", e) 
        """
        data_inicio = nav.find_element(By.XPATH,'//*[@id="from-modification-date-08d04454-5a5a-3436-9204-ba5b6abbaa27"]')
        data_inicio.send_keys(ontem)

        data_fim = nav.find_element(By.XPATH,'//*[@id="to-modification-date-08d04454-5a5a-3436-9204-ba5b6abbaa27"]')
        data_fim.send_keys(hoje)
        
        WebDriverWait(nav, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "knowledge-base-listing__article"))
        )
        
        i = 0
        dt = None
        titulo = None
        descricao = None
        pag = None

        while True:
            #try:
                # Atualiza a lista de datas
                WebDriverWait(nav, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "knowledge-base-listing__article"))
                )

                cves = nav.find_elements(By.CLASS_NAME, "knowledge-base-listing__article-title")
                
                if i >= len(cves):
                    break
                
                cve = cves[i]
                print(cves[i].get_attribute('innerHTML'))
                nav.execute_script("arguments[0].scrollIntoView(true);",cve)

                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'knowledge-base-listing__article-title')]"))
                )
                titulo = cve.find_element(By.XPATH, ".//a[contains(@class, 'knowledge-base-listing__article-title')]")
                print(titulo.text)
                '''
                    titulo_txt = titulo.text
                    titulo.click()

                    WebDriverWait(nav, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/p[1]'))
                    )

                    descricao = nav.find_element(By.XPATH, '//*[@id="content"]/p[1]').text
                    urgencia = nav.find_element(By.XPATH, '/html/body/div[1]/h3[4]').text
                    pag = nav.current_url
                    nav.back()
                    verificar_exite(dt, titulo_txt, descricao, urgencia, pag)

                    WebDriverWait(nav, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "date-tt"))
                    )
                else:
                    pass
                i += 1
                
            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                continue
    nav.quit()

def verificar_exite(data, titulo, descricao, urgencia, pag):
    nova = pd.DataFrame({"Data": [data], "Titulo":[titulo], "Descrição":[descricao],"Urgêcia": [urgencia], "Link pagina": [pag]}) 

    if os.path.exists(RELATORIO):
        try:
            df = pd.read_excel(RELATORIO)

        except Exception as e:
            print(f"----{e}-----")
            df = pd.DataFrame(columns=["Data","Titulo","Descrição", "Urgência", "Link pagina"])
            df.to_excel(RELATORIO, index=False)
 
    else:
        df = pd.DataFrame(columns=["Data","Titulo","Descrição","Urgência","Link pagina"])

    df = pd.concat([df, nova], ignore_index=True)
    df.to_excel(RELATORIO, index=False)

'''    

acessarSite()