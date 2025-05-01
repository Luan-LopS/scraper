import os # serve para trabalhar como arquivos/pasta de maquina
import pandas as pd #trabalhar com o excel 
from datetime import datetime # trabalhar com datas
import schedule # agendar execução
import time # sleep
from multiprocessing import Process, Queue, freeze_support #Processar em paralelo
from scrapers import palo_alto, splunk, qualys, trend, huawei # importa scrapers
import concurrent.futures 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv


USER = os.getenv("USERNAME")
RELATORIO = rf"C:\Users\{USER}\Desktop\Relatorio.xlsx"

def enviar_teams():
    pass


def enviar_email(resultado):
    load_dotenv()
    
    username = os.getenv('EMAIL_USER')
    senha = os.getenv('EMAIL_PASSWORD')
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    destinatario = 'luan.siqueira@compwire.com.br'
    assunto = 'CVES'
    corpo = f"Sergue relatios de cves do dia de hoje: {len(resultado)}"

    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"]= destinatario
    msg["Subject"] = assunto

    msg.attach(MIMEText(corpo,"plain"))

    with open(RELATORIO, "rb") as f:
        parte = MIMEApplication(f.read(), _subtype="xlsx")
        parte.add_header("Content-Disposition", "attachment", filename=os.path.basename(RELATORIO))
        msg.attach(parte)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as srv:
            srv.login(username,senha)
            srv.send_message(msg)
            print('Email enviado')
    except Exception as e:
        print('Erro:', e )



def gerandor_relatorio(resultado):
    print("Iniciando relatorio...")

    nova = pd.DataFrame(resultado) 

    if os.path.exists(RELATORIO):
        try:
            df = pd.read_excel(RELATORIO)

        except Exception as e:
            print(f"----{e}-----")
            df = pd.DataFrame(columns=[
                            'data',
                            'titulo',
                            'descição',
                            'urgencia',
                            'link'
                                        ])
            df.to_excel(RELATORIO, index=False)
 
    else:
        df = pd.DataFrame(columns=[
                            'data',
                            'titulo',
                            'descição',
                            'urgencia',
                            'link'
                                        ])

    df = pd.concat([df, nova], ignore_index=True)
    df.to_excel(RELATORIO, index=False)
    print("Finalizado relatorio")
    enviar_email(resultado)


def gereciador_scraping():
    
    with concurrent.futures.ProcessPoolExecutor() as executor:

        futuros = [
            executor.submit(palo_alto.scraper),
            executor.submit(splunk.scraper),
            executor.submit(qualys.scraper),
            executor.submit(trend.scraper),
            executor.submit(huawei.scraper)
        ]

        resultado = []
        for futuro in futuros:
            try:
                dados = futuro.result(timeout=60)
                resultado.extend(dados)
            except Exception as e:
                print(f"[MAIN] Erro ao processar scraper: {e}")

    if resultado:
        gerandor_relatorio(resultado)
    else:
        print("[MAIN] Nenhum resultado encontrado.")    


schedule.every(5).minutes.do(gereciador_scraping)

if __name__ == "__main__":
    gereciador_scraping()
    freeze_support()
    schedule.run_pending()
    time.sleep(60)
