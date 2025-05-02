from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date #datas


hoje = date.today() # dia de hoje 
pesquisa_data = hoje.strftime("%d/%m/%Y")
#pesquisa_data = '25/04/2025'
resultado = []
fabricante = 'GOOGLE'

def scraper():
    print("Iniciando scraper google...")
    options = Options()
    options.add_argument('--headless')  # Não abre o navegador
    #options.add_argument('--start-maximized')
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://cloud.google.com/support/bulletins?hl=pt-br"
    ]

    for pagina in paginas:
        nav.get(pagina) 

        WebDriverWait(nav, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "bulletins"))
        )         
        
        i = 0
        titulo = None
        descricao = None
        pag = None

        while True:
            try:  
                # Atualiza a lista de datas
                datas = nav.find_elements(By.XPATH, f'//*[@id="main-content"]/devsite-content/article/div[4]/section/p[contains(text(), "{pesquisa_data}")]')
                if i >= len(datas):
                    break
    
                data = datas[i]
                titulo = data.find_element(By.XPATH, "preceding-sibling::*[1]")
                tabela = data.find_element(By.XPATH,"following-sibling::*[2]")
                
                urgencia = tabela.find_element(By.XPATH, '//section/div/table/tbody/tr/td[2]').text
                link = tabela.find_element(By.XPATH, '//section/div/table/tbody/tr/td[3]/a')
                link.click()
                
                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="GeneratedTable"]/table/tbody/tr[4]/td'))
                )

                descricao = nav.find_element(By.XPATH,'//*[@id="GeneratedTable"]/table/tbody/tr[4]/td').text

                pag = nav.current_url
                nav.back()
              
                WebDriverWait(nav, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "bulletins"))
                )

                result = {
                    'data': pesquisa_data,
                    'titulo' :titulo,
                    'descição': descricao,
                    'urgencia': urgencia,
                    'link': pag
                    }
                    
                resultado.append(result)
                i += 1

            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                continue

    print("Finalizando scraper google.")
    
    nav.quit()
    #print(resultado)
    return resultado, fabricante

#scraper()