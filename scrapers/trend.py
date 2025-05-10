from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta #datas
import time

MES = {
    "janeiro": "01",
    "fevereiro": "02",
    "março": "03",
    "abril": "04",
    "maio": "05",
    "junho": "06",
    "julho": "07",
    "agosto": "08",
    "setembro": "09",
    "outubro": "10",
    "novembro": "11",
    "dezembro": "12"
}

resultado = []
ontem = datetime.now() - timedelta(days=1)
ULTIMA_CONSULTA = ontem.strftime("%Y-%m-%dT%H:%M:%S")
fabricante = 'TREND MICRO'
print(ULTIMA_CONSULTA)

def scraper():
    print("Iniciando scraper Trend...")
    options = Options()
    options.add_argument('--headless')  # Não abre o navegador
    options.add_argument('--disable-gpu')  # Necessário em alguns ambientes Windows
    options.add_argument('--no-sandbox')
    nav = webdriver.Chrome(options=options)
    paginas = [
            "https://www.trendmicro.com/vinfo/br/threat-encyclopedia/vulnerability/all-vulnerabilities"
        ]

    for pagina in paginas:
        nav.get(pagina)
        WebDriverWait(nav, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "descTitle"))
        )
    
        i = 0
        titulo = None
        descricao = None
        pag = None

        while True:
            try:
                tag_datas = nav.find_elements(By.CLASS_NAME, 'infoHead')
                if i >= len(tag_datas):
                    break

                data_pra_split = tag_datas[i].text
                data_split = data_pra_split.split(":")
                data = data_split[1].strip().lower().split()

                dia = data[0]
                mes = data[1]
                ano = data[2]

                mes_correto = MES.get(mes)
                dia_mes_ano = f"{dia} {mes_correto} {ano}"
                data_time = datetime.strptime(dia_mes_ano,"%d %m %Y")
                dt = data_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"000Z" 
             
                if dt > ULTIMA_CONSULTA:
                    
                    div = tag_datas[i].find_element(By.XPATH, "./ancestor::li")
                    link = div.find_element(By.XPATH, ".//a")
                    link.click()

                    WebDriverWait(nav, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="listDesc"]/div/b[1]'))
                    )
                    
                    titulo = nav.find_element(By.XPATH, '//section[1]/h1').text                  
                    #urgencia = nav.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div/table[2]/tbody/tr[2]/td[3]').text
                    #print('criticidade - ',urgencia)
                    descricao = nav.find_element(By.XPATH,'//*[@id="listDesc"]/div').text
                    pag = nav.current_url

                    nav.back()

                    WebDriverWait(nav,10).until(
                         EC.presence_of_element_located((By.CLASS_NAME, 'descTitle'))
                    )

                    result = {
                        'data': dt,
                        'titulo' :titulo,
                        'descição': descricao,
                        'urgencia': None,
                        'link': pag
                        }
                    
                    resultado.append(result)  # Colocando o resultado na fila

                else:
                     pass
                i += 1


            except (StaleElementReferenceException, NoSuchElementException, IndexError, ) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                continue            
            
    nav.quit()
    #print(resultado)
    print("Finalizado scraper Trend...")

    return resultado, fabricante

#scraper()