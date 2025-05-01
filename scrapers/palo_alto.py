from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime #datas


ULTIMA_CONSULTA = datetime.today() # dia de hoje 
resultado = []

def scraper():
    print("Iniciando scraper...")
    options = Options()
    options.add_argument('--headless')  # Não abre o navegador
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://security.paloaltonetworks.com/?sort=-date",
        "https://security.paloaltonetworks.com/?sort=-updated"
    ]

    for pagina in paginas:
        nav.get(pagina)
        WebDriverWait(nav, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "date-tt"))
        )   
        
        i = 0
        dt = None
        titulo = None
        descricao = None
        pag = None

        while True:
            try:
                # Atualiza a lista de datas
                datas = nav.find_elements(By.CLASS_NAME, "date-tt")
                if i >= len(datas):
                    break
                
                data = datas[i]
                dt = data.get_attribute('data-date')                
                dt_formatado = ULTIMA_CONSULTA.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

                if dt > dt_formatado:
                    linha = data.find_element(By.XPATH, "./ancestor::tr")
                    titulo = linha.find_element(By.XPATH, ".//a")
                    titulo.click()

                    WebDriverWait(nav, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/p[1]'))
                    )

                    descricao = nav.find_element(By.XPATH, '//*[@id="content"]/p[1]').text
                    urgencia = nav.find_element(By.XPATH, '/html/body/div[1]/h3[4]').text
                    pag = nav.current_url
                    nav.back()
                    
                    WebDriverWait(nav, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "date-tt"))
                    )

                    result = {
                        'data': dt,
                        'titulo' :titulo.text,
                        'descição': descricao,
                        'urgencia': urgencia,
                        'link': pag
                        }
                    
                    resultado.append(result)
                    i += 1


                else:
                    pass
                i += 1
                
            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                continue

    print("Finalizando scraper.")
    
    nav.quit()
#    print(resultado)
    return resultado
    
#scraper()