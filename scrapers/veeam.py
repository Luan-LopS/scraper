from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta
from time import sleep 

hoje = date.today().strftime('%d-%m-%Y') #'09-04-2025'
o = date.today() - timedelta(days=1)
ontem = o.strftime('%d-%m-%Y')      #'08-04-2025'
fabricante = 'VEEAM'
resultado = []

def scraper():
    print("Iniciando scraper Veeam...")
    options = Options()
    options.add_argument('--headless')

    #options.add_argument("--start-maximized") 
    nav = webdriver.Chrome(options=options)
    paginas = [
        "https://www.veeam.com/kb"
    ]

    for pagina in paginas:
        nav.get(pagina)

        WebDriverWait(nav, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "knowledge-base-listing__article"))
        )
        
        data_inicio = nav.find_element(By.XPATH,'//*[@id="from-modification-date-08d04454-5a5a-3436-9204-ba5b6abbaa27"]')
        data_inicio.send_keys(ontem)

        data_fim = nav.find_element(By.XPATH,'//*[@id="to-modification-date-08d04454-5a5a-3436-9204-ba5b6abbaa27"]')
        data_fim.send_keys(hoje)

        i = 0
        dt = hoje
        titulo = None
        descricao = None
        urgencia= None
        pag = None

        while True:
            try:
                # Atualiza a lista de datas
                WebDriverWait(nav, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "knowledge-base-listing__article"))
                )

                sleep(2)

                cves = nav.find_elements(By.CLASS_NAME, "knowledge-base-listing__article-title")

                if i >= len(cves):
                    break
                
                cve = cves[i]
                nav.execute_script("arguments[0].scrollIntoView(true);",cve)
                nav.execute_script("arguments[0].click();", cve)

                #//*[@id="_qualified-offer-dismiss-button-1604351994528006982"]
                
                WebDriverWait(nav, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h1"))
                )

                titulo = nav.find_element(By.XPATH, "//h1").text
                desc1 = nav.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div[2]')
                if desc1:
                    descricao = desc1[0].text

                # Segunda tentativa, se a primeira falhar
                if not descricao:
                    desc2 = nav.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/div/div/div/div/div[3]/div/div/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div[2]/div')
                    if desc2:
                        descricao = desc2[0].text

                # Terceira tentativa, se as duas anteriores falharem
                if not descricao:
                    desc3 = nav.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/div/div/div/div/div[3]/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div[3]/div/div')
                    if desc3:
                        descricao = desc3[0].text

                pag = nav.current_url
                nav.back()

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

    print("Finalizado scraper Veeam...")

    nav.quit()
    #print(resultado)
    return resultado, fabricante

#scraper()