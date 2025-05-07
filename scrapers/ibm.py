from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import date #datas

hoje = date.today() # dia de hoje 
pesquisa_data = hoje.strftime("%Y-%m-%d")
#pesquisa_data = '21/04/2025'
ano_atual = hoje.year
resultado = []
fabricante = 'IBM'

def scraper():
    print("Iniciando scraper IBM...")
    options = Options()
    options.add_argument('--headless')  # Não abre o navegador
    #options.add_argument('--start-maximized')
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://www.ibm.com/support/pages/bulletin/"
    ]

    for pagina in paginas:
        nav.get(pagina)        
             
        WebDriverWait(nav, 20).until(
                    EC.presence_of_element_located((By.ID, "datatable"))
        )
       
        quantidade_linha = nav.find_element(By.XPATH, '//*[@id="datatable_length"]/label/select')
        select = Select(quantidade_linha)
        select.select_by_visible_text('100')
        
        i = 0
        dt = pesquisa_data
        titulo = None
        urgencia = None
        descricao = None
        pag = None
        cont = 0
        j = 0

        while True:
            try:   
                # Atualiza a lista de datas
                datas = nav.find_elements(By.XPATH, f"//*[@id='datatable']/tbody/tr/td[5][contains(text(), '{pesquisa_data}')]")
                if cont == 0:
                    cont = len(datas)

                if j >= cont:
                    break
                                   
                data = datas[i]
                urgencia = data.find_element(By.XPATH, "preceding-sibling::td[1]").text
                titulo = data.find_element(By.XPATH, 'preceding-sibling::td[4]').text
                link = data.find_element(By.XPATH, 'preceding-sibling::td[4]/a')
                nav.execute_script("arguments[0].removeAttribute('target')", link)
                nav.execute_script("arguments[0].click();", link)

                WebDriverWait(nav, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'bx--row'))
                )

                descricao = nav.find_element(By.XPATH, '//*[@id="com.dblue.docview.body.content"]/div/div/div/div[1]/p').text
                pag = nav.current_url
                nav.back()
                    
                WebDriverWait(nav, 15).until(
                    EC.presence_of_element_located((By.ID, "datatable"))
                )

                quantidade_linha = nav.find_element(By.XPATH, '//*[@id="datatable_length"]/label/select')
                select = Select(quantidade_linha)
                select.select_by_visible_text('100')

                result = {
                    'data': dt,
                    'titulo' :titulo,
                    'descrição': descricao,
                    'urgencia': urgencia,
                    'link': pag
                    }
                    
                resultado.append(result)

                i += 1
                j += 1                    

                if j >= cont:
                    pagina = nav.find_element(By.XPATH, '//*[@id="datatable_next"]')
                    nav.execute_script("arguments[0].click();", pagina)
                    WebDriverWait(nav, 20).until(
                        EC.presence_of_element_located((By.ID, "datatable"))
                    )

                    quantidade_linha = nav.find_element(By.XPATH, '//*[@id="datatable_length"]/label/select')
                    select = Select(quantidade_linha)
                    select.select_by_visible_text('100')
                    datas = nav.find_elements(By.XPATH, f"//*[@id='datatable']/tbody/tr/td[5][contains(text(), '{pesquisa_data}')]")
                    i = 0
                    cont += len(datas)

            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                j +=1
                continue

    print("Finalizando scraper IBM.")
    
    nav.quit()
    #print(resultado)
    return resultado, fabricante

scraper()