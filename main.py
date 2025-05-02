import os# serve para trabalhar como arquivos/pasta de maquina
import sys
import pandas as pd #trabalhar com o excel 
from datetime import datetime # trabalhar com datas
import schedule # agendar execução
import time # sleep
from multiprocessing import freeze_support #Processar em paralelo
from scrapers import palo_alto, splunk, qualys, trend, huawei, aws, google, oragle, dynatrace, ibm # importa scrapers
import concurrent.futures 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv, find_dotenv
from io import BytesIO
from xlsxwriter import Workbook
import requests

webhook_url = "https://compwirecombr.webhook.office.com/webhookb2/446415a8-43f6-4b9f-9fef-1701fe1fb814@4459998e-7581-4529-973d-e4738fe9a2a9/IncomingWebhook/8b137d6764374128836390171a438279/f87bd603-b64d-46e1-a813-4310327057dd/V2H1BBBzX7OUNFNMa5oq7ZTsbNFksd9AkG1B1f6ut688w1"
mensagem = "✅ Scraping e envio de e-mail concluídos com sucesso!"
 

def enviar_teams(mensagem, webhook_url):
    payload = {"text": mensagem}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Mensagem enviada com sucesso ao Teams.")
    else:
        print(f"Erro ao enviar para Teams: {response.status_code} - {response.text}")

# Exemplo de uso

def enviar_email(resultado, excel_buffer):
    if getattr(sys, 'frozen', False):  # executável
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    dotenv_path = os.path.join(base_path, '.env')
    load_dotenv(dotenv_path)
    
    username = os.getenv('EMAIL_USER')
    senha = os.getenv('EMAIL_PASSWORD')

    if not username or not senha:
        print('erro')

    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    destinatarios = ['luan.siqueira@compwire.com.br','vinicius.clemente@compwire.com.br', '']
    assunto = 'CVES'
    corpo = f"Segue relatios de cves do dia de hoje: {len(resultado)}"

    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"]= ', '.join(destinatarios)
    msg["Subject"] = assunto

    msg.attach(MIMEText(corpo,"plain"))

     # Anexa o Excel da memória
    parte = MIMEApplication(excel_buffer.read(), _subtype="xlsx")
    parte.add_header("Content-Disposition", "attachment", filename="relatorio_cves.xlsx")
    msg.attach(parte)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as srv:
            srv.login(username, senha)
            srv.send_message(msg)
            print('Email enviado')

        enviar_teams(mensagem, webhook_url)
    except Exception as e:
        print('Erro ao enviar e-mail:', e)


def gerandor_relatorio(resultado, fabricante):
    print("Iniciando relatorio...")

    excel = pd.DataFrame(resultado) 

    colunas=['data', 'titulo', 'descrição', 'urgencia', 'link']
    if not all (col in excel.columns for col in colunas):
        excel = excel.reindex(columns=colunas)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        for fab in fabricante:
        excel.to_excel(writer, index=False, sheet_name=fabricante)
    buffer.seek(0)

    print("Relatório pronto. Enviando por e-mail...")
    enviar_email(resultado, buffer)


def gereciador_scraping():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        futuros = [
            executor.submit(palo_alto.scraper),
            executor.submit(splunk.scraper),
            executor.submit(qualys.scraper),
            executor.submit(trend.scraper),
            executor.submit(huawei.scraper),
            executor.submit(aws.scraper),
            executor.submit(google.scraper),
            executor.submit(oragle.scraper),
            executor.submit(dynatrace.scraper),
            executor.submit(ibm.scraper)
        ]

        resultado = []
        for futuro in futuros:
            try:
                dados, fabricante = futuro.result(timeout=2000)
                resultado.extend(dados)
            except Exception as e:
                print(f"[MAIN] Erro ao processar scraper: {e}")

    if resultado:
        gerandor_relatorio(resultado, fabricante)
    else:
        print("[MAIN] Nenhum resultado encontrado.")
        gerandor_relatorio(resultado, fabricante)

schedule.every(4).hours.do(gereciador_scraping)

if __name__ == "__main__":
    gereciador_scraping()
    freeze_support()

    while True:
        schedule.run_pending()
        time.sleep(60)
