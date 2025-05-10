from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date
import time 

hoje_str = date.today()
hoje = hoje_str.strftime('%Y.%m.%d')
ano = '2025'
fabricante = 'HUAWEI'
resultado = []

def scraper():
    options = Options()
    options.add_argument('--headless')  # Não abre o navegador
    options.add_argument('--disable-gpu')  # Necessário em alguns ambientes Windows
    options.add_argument('--no-sandbox')
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://www.huawei.com/br/psirt/all-bulletins"
    ]
    for pagina in paginas:
        nav.get(pagina)
        
        WebDriverWait(nav, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content_1_divBulletinsList"]/div[1]/div[1]/dl/dd[2]/ul[1]/li[1]/p'))
        )

        i = 0
        dt = None
        titulo = None
        descricao = None
        urgencia=None
        pag = None

        while True:
            try:
                # Atualiza a lista de datas
                ano_click = nav.find_element(By.XPATH, '//*[@id="content_1_divBulletinsList"]/div[1]/div[1]/dl/dd[2]/ul[1]/li[1]/p')
                if ano == ano_click.text.split(" ")[0]: ano_click.click()   

                WebDriverWait(nav, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tbContent"]/li'))
                )  

                cves = nav.find_elements(By.XPATH, '//*[@id="tbContent"]/li')
                if i >= len(cves):
                    break
                    
                cve = cves[i].find_element(By.XPATH, './/a')
                data = cve.find_element(By.XPATH, './/p').text.split(" | ")[1]
                dt = data.strip().split(' ')[0]       
                    #2025.03.26                  

                if (dt == hoje):  
                      
                    cve.click()
                    
                    WebDriverWait(nav, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[4]/div/div[1]/h1'))
                    )

                    pag = nav.current_url
                    titulo = nav.find_element(By.XPATH,'//*[@id="container"]/div[4]/div/div[1]/h1').text
                    descricao = nav.find_element(By.XPATH,'//*[@id="container"]/div[4]/div/div[1]/div[2]/div[1]/div[2]').text
                    urgencia = nav.find_element(By.XPATH,'//*[@id="container"]/div[4]/div/div[1]/div[2]/div[4]/div[2]/p[3]').text

                    nav.back()
                                         
                    WebDriverWait(nav, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="content_1_divBulletinsList"]/div[1]/div[1]/dl/dd[2]/ul[1]/li[1]/p'))
                    )

                    result = {
                        'data': dt,
                        'titulo' :titulo,
                        'descição': descricao,
                        'urgencia': urgencia,
                        'link': pag
                        }
                    
                    resultado.append(result)  # Colocando o resultado na fila

                    i += 1
                else:
                    print(f'Data não encontrada {hoje}, ultima data {dt}')
                    break
                       
            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                    print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                    i += 1
                    continue    
       
    nav.quit()
#    print(resultado)
    print("Finalizado scraper Huawei...")
    return resultado, fabricante

#scraper()