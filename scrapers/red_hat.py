from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import date #datas
from time import sleep

hoje = date.today() # dia de hoje 
pesquisa_data = hoje.strftime("%d/%m/%Y")
print(pesquisa_data)
resultado = []
fabricante = 'RED HAT'
#    "https://access.redhat.com/security/",

def scraper():
    print("Iniciando scraper RED HAT...")
    options = Options()
    #options.add_argument('--headless')

    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://access.redhat.com/security/security-updates/cve?q=&p=1&sort=cve_publicDate+desc,allTitle+desc&rows=100&documentKind=Cve"
    ]

    for pagina in paginas:
        nav.get(pagina)        

        WebDriverWait(nav, 20).until(
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

        WebDriverWait(nav, 10).until(
            EC.visibility_of_element_located((By.ID, 'cve-db-table'))
        )
       
        datas = nav.find_elements(By.XPATH, '//*[@id="cve-db-table"]/cp-tbody/cp-tr/cp-td[3]')
        
        controle=[]
        for data in datas:
            if data.text == pesquisa_data:
                controle.append(data)
        sleep(1)

        i = 0
        titulo = None
        urgencia = ""
        descricao = None
        pag = None

        while True:
            try:
                if i >= len(controle):
                    break
                
                data = controle[i]
                linha = nav.find_element(By.XPATH, f'//*[@id="cve-db-table"]/cp-tbody/cp-tr[{i+1}]')
                titulo = linha.find_element(By.XPATH,'./cp-th')
                descricao = linha.find_element(By.XPATH, './cp-td[1]').text
                urgencia = linha.find_element(By.XPATH,'./cp-td[2]').text
                data = linha.find_element(By.XPATH, './cp-td[3]').text
                link = titulo.find_element(By.XPATH, './a')
                pag = link.get_attribute('href')

                result = {
                        'data': pesquisa_data,
                        'titulo' :titulo.text,
                        'descrição': descricao,
                        'urgencia': urgencia,
                        'link': pag
                }

                resultado.append(result)

                i+=1

            except (StaleElementReferenceException, NoSuchElementException, IndexError) as e:
                print(f"Erro com o elemento ou índice fora do alcance: {e}. Continuando.")
                i += 1
                continue

    print("Finalizando scraper RED HAT.")
    
    nav.quit()
    #print(resultado)
    return resultado, fabricante
    
#scraper()
