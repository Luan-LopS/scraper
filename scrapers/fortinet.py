# https://www.fortiguard.com/psirt

from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date #datas

hoje = date.today() 
pesquisa_data = hoje.strftime("%b %d,%Y")
print(pesquisa_data)
ano_atual = hoje.year
resultado = []
fabricante = 'FORTINET'

def scraper():
    print("Iniciando scraper FORTINET...")
    options = Options()
    options.add_argument('--headless')  # Não abre o navegador
    #options.add_argument('--start-maximized')
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://www.fortiguard.com/psirt"
    ]

    for pagina in paginas:
        nav.get(pagina)        

        WebDriverWait(nav, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "container-xxl"))
        )

        ano_click = nav.find_element(By.XPATH, f'//*[@id="full-page"]/section[2]/div/div[1]/div/form/div/div[3]/div/span[2]/span[1]/span')
        ano_click.send_keys(ano_atual)
        ano_click.send_keys('\ue004')
        
        i = 0
        dt = None
        titulo = None
        descricao = None
        urgencia = None
        pag = None

        while True:
            try:
                WebDriverWait(nav, 15).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="full-page"]/section[3]/div/div/div[4][contains(., "{pesquisa_data}")]'))
                )

                datas = nav.find_elements(By.XPATH, f'//*[@id="full-page"]/section[3]/div/div/div[4][contains(., "{pesquisa_data}")]')
                if i >= len(datas):
                    break

                data = datas[i]
                urgencia = data.find_element(By.XPATH, './following-sibling::div[4]').text
                descricao = data.find_element(By.XPATH, './preceding-sibling::div[2]').text
                titulo = data.find_element(By.XPATH, './preceding-sibling::div[3]').text
                link = data.find_element(By.XPATH, '//*[@id="full-page"]/section[3]/div/div[1]')
                nav.execute_script("arguments[0].removeAttribute('target')", link)
                nav.execute_script("arguments[0].click();", link)

                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'title'))
                )

                pag = nav.current_url

                nav.back()

                WebDriverWait(nav, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "container-xxl"))
                )

                ano_click = nav.find_element(By.XPATH, f'//*[@id="full-page"]/section[2]/div/div[1]/div/form/div/div[3]/div/span[2]/span[1]/span')
                ano_click.send_keys(ano_atual)
                ano_click.send_keys('\ue004')

                result = {
                    'data': dt,
                    'titulo' :titulo,
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

            except TimeoutException as error:
                print("Elemento não existente")
                break


    print("Finalizando scraper FORTINET.")
    
    nav.quit()
    #print(resultado)
    return resultado, fabricante
    
#scraper()