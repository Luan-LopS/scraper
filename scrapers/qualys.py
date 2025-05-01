from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime #datas

ULTIMA_CONSULTA = datetime.today()  # dia atual
resultado=[]

def scraper():
    options = Options()
    options.add_argument('--headless')  # Não abre o navegador
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://www.qualys.com/security-advisories/"
        ]

    for pagina in paginas:
        nav.get(pagina)
        WebDriverWait(nav, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "publication-date"))
        )
    
        i = 0
        titulo = None
        descricao = None
        pag = None

        while True:
            try:
                datas = nav.find_elements(By.CLASS_NAME, "publication-date")

                if i >= len(datas):
                    break

                data = datas[i]
                data_time = datetime.strptime(data.text,"%b %d, %Y")
                dt = data_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"000Z" 
                dt_formatado = ULTIMA_CONSULTA.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
               
                if data_time > ULTIMA_CONSULTA:
                    div = nav.find_element(By.CLASS_NAME, "q-grid__inner") # q-advisories__container-inner
                    link = div.find_element(By.XPATH, ".//a")
                    nav.execute_script("arguments[0].scrollIntoView(true);", link)
                    nav.execute_script("arguments[0].click();", link)

                    WebDriverWait(nav, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[1]/div/h2'))
                    )

                    titulo = nav.find_element(By.XPATH, '/html/body/main/div/div/div[1]/div/h2').text
                    urgencia = nav.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div/table[2]/tbody/tr[2]/td[3]').text
                    descricao = nav.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div/p[1]').text
                    pag = nav.current_url

                    nav.back()

                    WebDriverWait(nav,10).until(
                         EC.presence_of_element_located((By.CLASS_NAME, 'publication-date'))
                    )

                    result = {
                        'data': dt,
                        'titulo' :titulo,
                        'descição': descricao,
                        'urgencia': urgencia,
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
#    print(resultado)
    return resultado

#scraper()