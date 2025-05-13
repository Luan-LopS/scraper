from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date #datas
from time import sleep


hoje = date.today() # dia de hoje 
pesquisa_data = hoje.strftime("%d/%m/%Y")
#pesquisa_data = '21/04/2025'
ano_atual = hoje.year
resultado = []
fabricante = 'IVANTI'

def scraper():
    print("Iniciando scraper IVANTI...")
    options = Options()
    options.add_argument('--headless')

    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://www.ivanti.com/en-us/security-advisories"
    ]

    for pagina in paginas:
        nav.get(pagina)        
        ano_click = nav.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{ano_atual}']")
        ano_click.click()
      
        WebDriverWait(nav, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "m-card-title"))
        )
        
        i = 0
        dt = None
        titulo = None
        descricao = None
        pag = None

        while True:
            try:  
                # Atualiza a lista de datas
                datas = nav.find_elements(By.XPATH, f"//*[contains(@class, 'm-card-info') and contains(text(), '{pesquisa_data}')]")
                if i >= len(datas):
                    break

                data = datas[i]
                div_pai = data.find_element(By.XPATH, "./ancestor::div")

                #link = div_pai.find_element(By.XPATH, '//section//ul/li[1]//a')
                #nav.execute_script("arguments[0].removeAttribute('target')", link)
                #nav.execute_script("arguments[0].click();", link)

                #WebDriverWait(nav, 10).until(
                #    EC.presence_of_element_located((By.CLASS_NAME, 'title'))
                #)

                #titulo = nav.find_element(By.CLASS_NAME,'title').text

                #descricao = nav.find_element(By.XPATH, '//section//div[3]/div').text
                #urgencia = nav.find_element(By.XPATH, '/html/body/div[1]/h3[4]').text
                #pag = nav.current_url
                #nav.back()
                    
                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "m-card-title"))
                )

                ano_click = nav.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{ano_atual}']")
                ano_click.click()

                result = {
                    'data': dt,
                    'titulo' :titulo,
                    'descrição': descricao,
                    'urgencia': None,
                    'link': pag
                    }
                    
                resultado.append(result)
                i += 1

            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                continue

    print("Finalizando scraper IVANTE.")
    
    nav.quit()
    #print(resultado)
    return resultado, fabricante
    
#scraper()