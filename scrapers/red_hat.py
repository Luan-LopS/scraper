from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import date #datas
from time import sleep

hoje = date.today() # dia de hoje 
pesquisa_data = hoje.strftime("%Y-%m-%d")
#pesquisa_data = '21/04/2025'
ano_atual = hoje.year
resultado = []

def scraper():
    print("Iniciando scraper RED HAT...")
    options = Options()
    #options.add_argument('--headless')  # Não abre o navegador
    options.add_argument('--start-maximized')
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://access.redhat.com/security/",
        "https://access.redhat.com/security/security-updates/cve?q=&p=1&sort=cve_publicDate+desc,allTitle+desc&rows=100&documentKind=Cve"
    ]

    for pagina in paginas:
        nav.get(pagina)        

        WebDriverWait(nav, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div'))
        )

        iframe1 = WebDriverWait(nav, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "truste_popframe"))
        )
        nav.switch_to.frame(iframe1)

        WebDriverWait(nav, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="pdynamicbutton"]/a[2]'))
        )

        nav.find_element(By.XPATH, '//div[@class="pdynamicbutton"]/a[2]').click()
        sleep(20)


        '''
       
        quantidade_linha = nav.find_element(By.XPATH, '//*[@id="datatable_length"]/label/select')
        select = Select(quantidade_linha)
        select.select_by_visible_text('100')
        
        i = 0
        dt = None
        titulo = None
        urgencia = None
        descricao = None
        pag = None
        cont = 0

        while True:
            try:   
                # Atualiza a lista de datas
                datas = nav.find_elements(By.XPATH, f"//*[@id='datatable']/tbody/tr/td[5][contains(text(), '{pesquisa_data}')]")
                if cont == 0:
                    cont = len(datas)
                print(f"Cont {cont}" )
                print(f"Datas {len(datas)}" )
                print(f"I {i}" )

                if i >= cont:
                    break
                                   
                data = datas[i]
                urgencia = data.find_element(By.XPATH, "preceding-sibling::td[1]").text
                titulo = data.find_element(By.XPATH, 'preceding-sibling::td[4]').text
                link = data.find_element(By.XPATH, 'preceding-sibling::td[4]/a')
                nav.execute_script("arguments[0].removeAttribute('target')", link)
                nav.execute_script("arguments[0].click();", link)

                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'bx--row'))
                )

                descricao = nav.find_element(By.XPATH, '//*[@id="com.dblue.docview.body.content"]/div/div/div/div[1]/p')
                pag = nav.current_url
                nav.back()
                    
                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.ID, "datatable"))
                )

                quantidade_linha = nav.find_element(By.XPATH, '//*[@id="datatable_length"]/label/select')
                select = Select(quantidade_linha)
                select.select_by_visible_text('100')

                result = {
                    'data': dt,
                    'titulo' :titulo,
                    'descição': descricao,
                    'urgencia': urgencia,
                    'link': pag
                    }
                    
                resultado.append(result)
                
                i += 1                    

                if i >= len(datas):
                    pagina = nav.find_element(By.XPATH, '//*[@id="datatable_next"]')
                    pagina.click()
                    cont += len(datas)

            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                continue

    print("Finalizando scraper IBM.")
    
    nav.quit()
    print(resultado)
    return resultado
'''
scraper()