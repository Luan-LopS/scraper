from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date #datas

hoje = date.today() # dia de hoje // 21 April 2025
pesquisa_data =  hoje.strftime("%d %B %Y")
ano_atual = hoje.year
resultado = []
fabricante = 'ORACLE'

def scraper():
    print("Iniciando scraper oracle...")
    options = Options()
    options.add_argument('--headless')  # Não abre o navegador
    options.add_argument('--disable-gpu')  # Necessário em alguns ambientes Windows
    options.add_argument('--no-sandbox')
    #options.add_argument('--start-maximized')
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://www.oracle.com/security-alerts/"
    ]

    for pagina in paginas:
        nav.get(pagina)
        WebDriverWait(nav, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "cc02v4"))
        )   
        
        i = 0
        dt = pesquisa_data
        titulo = None
        descricao = None
        urgencia =None
        pag = None

        while True:
            try:
                WebDriverWait(nav, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'otable-w1'))
                )

                datas = nav.find_elements(By.XPATH, f"//table/tbody/tr/td[2][contains(text(), '{pesquisa_data}')]")
                if i >= len(datas):
                    break
                
                data = datas[i]
                
                linha = data.find_element(By.XPATH, "preceding-sibling::td")
                link = linha.find_element(By.XPATH, ".//a")
                link.click()

                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'cwidth'))
                )

                titulo = nav.find_element(By.XPATH,'/html/body/div[2]/section[2]/div/h2').text
                descricao = nav.find_element(By.XPATH, '/html/body/div[2]/section[2]/div/p[1]').text
                #urgencia = nav.find_element(By.XPATH, '/html/body/div[1]/h3[4]').text
                pag = nav.current_url
                nav.back()
                    
                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cc02v4"))
                )

                result = {
                    'data': dt,
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

    print("Finalizando scraper oracle.")
    
    nav.quit()
#    print(resultado)
    return resultado, fabricante

#scraper()