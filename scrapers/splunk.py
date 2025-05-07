from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date

ULTIMA_CONSULTA = datetime(2025, 4, 10, 12, 0, 0)  # ano, mês, dia, hora, minuto, segundo TESTES
hoje = str(date.today())
resultado = []
fabricante = 'SPLUK'

def scraper():
    print("Iniciando scraper splunk...")

    options = Options()
    options.add_argument('--headless')  # Não abre o navegador
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://advisory.splunk.com/"
    ]

    for pagina in paginas:
        nav.get(pagina)


        WebDriverWait(nav, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="advisory-table-all_wrapper"]/div[2]/div[1]/div/div[2]/button'))
        )   

        search = nav.find_element(By.XPATH,'//*[@id="advisory-table-all_filter"]/label/input')
        search.send_keys(hoje)        

        try:
            WebDriverWait(nav, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sorting_2"))
            )  

        except (Exception, TimeoutError) as e:
            print(f'Elemento {e} não existente')
            nav.quit
            break

        i = 0
        dt = None
        titulo = None
        descricao = None
        urgencia=None
        pag = None

        while True:
            try:
                # Atualiza a lista de datas
                cves = nav.find_elements(By.CLASS_NAME, "sorting_2")
                if i >= len(cves):
                    break
                
                dt = nav.find_element(By.XPATH,'//td[@label="Published"]').text
                urgencia = nav.find_element(By.XPATH,'//td[@label="Severity"]').text
                nav.execute_script("arguments[0].scrollIntoView(true);", cves[i])
                nav.execute_script("arguments[0].click();", cves[i])
                cves[i].click()
                
                WebDriverWait(nav, 15).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="advisory"]/div[1]/h1'))
                    )
                
                titulo = nav.find_element(By.XPATH,'//*[@id="advisory"]/div[1]/h1').text
                descricao = nav.find_element(By.XPATH,'//*[@id="advisory"]/div[3]/p[1]').text
                pag = nav.current_url
                
                nav.back()

                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "sorting_2"))
                )

                i += 1

                result = {
                        'data': dt,
                        'titulo' :titulo,
                        'descrição': descricao,
                        'urgencia': urgencia,
                        'link': pag
                        }
                
                resultado.append(result)  # Colocando o resultado na fila

            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                continue

    print("Finalizando scraper splunk.")
    nav.quit()
#    print(resultado)

    return resultado, fabricante


#scraper()