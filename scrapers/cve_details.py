# https://www.cvedetails.com/vulnerability-list/year-2025/month-5/May.html?page=1&order=7


from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date #datas
from time import sleep

hoje = date.today() # dia de hoje 
pesquisa_data = hoje.strftime("%d/%B/%Y")
mes = pesquisa_data.split('/')
mes = mes[1]
pesquisa_data = hoje.strftime("%Y-%m-%d")

mes_numero = hoje.month
ano_atual = hoje.year
resultado = []
fabricante = 'CVE_DETAILS'

paginas = []
URL =  f"https://www.cvedetails.com/vulnerability-list/year-{ano_atual}/month-{mes_numero}/{mes}.html?page=1&order=7"
paginas.append(URL)


def scraper():
    print("Iniciando scraper CVE_DETAILS...")
    options = Options()
    options.add_argument('--headless')
    #options.add_argument('--start-maximized')
    nav = webdriver.Chrome(options=options)
   
    for pagina in paginas:
        nav.get(pagina)
         
        cookie = WebDriverWait(nav, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cookieconsentwarning"]/div[2]/a[1]'))
        ) 
        cookie.click()
       
        i = 0
        dt = pesquisa_data
        titulo = None
        descricao = None
        urgencia = None
        pag = None

        while True:
            try:
                # Atualiza a lista de datas
                cves = WebDriverWait(nav, 15).until(
                    EC.presence_of_all_elements_located((By.XPATH, f".//div[contains(@class, 'hover-bg-light') and contains(., '{pesquisa_data}')]"))
                ) 

                if i >= len(cves):
                    break
                
                cve = cves[i]

                titulo = cve.find_element(By.XPATH, './/h3')
                link = titulo.find_element(By.TAG_NAME, 'a')
                pag = link.get_attribute('href')
                
                descricao = cve.find_element(By.XPATH, './/div[2]').text
                CVSS = cve.find_element(By.XPATH, './/div[2]/div[2]')
                CVSS = CVSS.text.replace('\n', ' ')
                EPSS = cve.find_element(By.XPATH, './/div[2]/div[1]')
                EPSS = EPSS.text.replace('\n', ' ')

                urgencia = {
                    'CVSS': CVSS,
                    'EPSS': EPSS
                }

                
                result = {
                    'data': dt,
                    'titulo' :titulo.text,
                    'descrição': descricao,
                    'urgencia': urgencia,
                    'link': pag
                    }
                    
                resultado.append(result)
                i += 1

            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                continue

    print("Finalizando scraper CVE_DETAILS.")
    
    nav.quit()
    #print(resultado)
    return resultado, fabricante
    
#scraper()


