import os# serve para trabalhar como arquivos/pasta de maquina
import sys
import pandas as pd #trabalhar com o excel 
from datetime import datetime # trabalhar com datas
import schedule # agendar execução
import time # sleep
import requests
from dotenv import load_dotenv
from multiprocessing import freeze_support #Processar em paralelo
import concurrent.futures 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from io import BytesIO
from mensagem import html
from scrapers import palo_alto, splunk, qualys, trend, huawei, aws, google, oragle, dynatrace, ibm, red_hat, fortinet, veeam, cve_details # importa scrapers


if getattr(sys, 'frozen', False):  # executável
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

dotenv_path = os.path.join(base_path, '.env')
load_dotenv(dotenv_path)

username = os.getenv('EMAIL_USER')
senha = os.getenv('EMAIL_PASSWORD')
webhook_url = os.getenv('WEBHOOK_URL')


def enviar_teams(resultado):
    mensagem = html.teams(resultado)
    payload = {"text": mensagem}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Mensagem enviada com sucesso ao Teams.")
    else:
        print(f"Erro ao enviar para Teams: {response.status_code} - {response.text}")


# Exemplo de uso
def enviar_email(resultado, excel_buffer):
    if not username or not senha:
        print('erro')

    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    destinatarios = ['luan.siqueira@compwire.com.br','vinicius.clemente@compwire.com.br','thiago.mendes@compwire.com.br','fabio.aquino@compwire.com.br', 'isaac.santos@compwire.com.br', 'marcio.oliveira@compwire.com.br']
    assunto = 'Relatorio de CVES'

    corpo = html.email(resultado)

    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"]= ', '.join(destinatarios)
    msg["Subject"] = assunto

    msg.attach(MIMEText(corpo,'html'))

    parte = MIMEApplication(excel_buffer.read(), _subtype="xlsx")
    parte.add_header("Content-Disposition", "attachment", filename="relatorio_cves.xlsx")
    msg.attach(parte)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as srv:
            srv.login(username, senha)
            srv.send_message(msg)
            print('Email enviado')

        enviar_teams(resultado)
    except Exception as e:
        print('Erro ao enviar e-mail:', e)


def gerador_relatorio(resultado, fabricantes):
    print("Iniciando relatorio...")

    excel = pd.DataFrame(resultado) 
    colunas=['data', 'titulo', 'descrição', 'urgencia', 'link']
    for col in colunas:
        if col not in excel.columns:
            excel[col] = None

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

        for fabricante in fabricantes:
            df_filtro = excel[excel['fabricante'] == fabricante]
            
            remove_dupicados = df_filtro.drop_duplicates(subset=['descrição', 'data', 'link'])
            remove_dupicados.to_excel(writer, index=False, sheet_name=fabricante[:31])
    buffer.seek(0)

    print("Relatório pronto. Enviando por e-mail...")
    enviar_email(resultado, buffer)


def gereciador_scraping():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:

        futuros = [
            executor.submit(palo_alto.scraper),  #1
            executor.submit(splunk.scraper),     #2
            executor.submit(qualys.scraper),     #3
            executor.submit(trend.scraper),      #4
            executor.submit(huawei.scraper),     #5
            executor.submit(aws.scraper),        #6
            executor.submit(google.scraper),     #7
            executor.submit(oragle.scraper),     #8
            executor.submit(dynatrace.scraper),  #9
            executor.submit(ibm.scraper),        #10
            executor.submit(red_hat.scraper),    #11
            executor.submit(fortinet.scraper),   #12
            executor.submit(veeam.scraper),      #13
            # ivant cadastrar                    #14
            # CloudFlare github                  #15
            # Apura não tem site                 #16
            # Cloudera cadastrar                 #17
            executor.submit(cve_details.scraper) #18
        ]

        resultado = []
        fabricantes = []
        for futuro in futuros:
            try:
                dados, fabricante = futuro.result(timeout=2000)

                for item in dados:
                    item['fabricante'] = fabricante

                resultado.extend(dados)
                fabricantes.append(fabricante)
            except Exception as e:
                print(f"[MAIN] Erro ao processar scraper: {e}")

    if resultado:
        gerador_relatorio(resultado, fabricantes)
    else:
        print("[MAIN] Nenhum resultado encontrado.")
        gerador_relatorio(resultado, fabricantes)


schedule.every(2).hours.do(gereciador_scraping)



if __name__ == "__main__":
    gereciador_scraping()
    freeze_support()

    while True:
        schedule.run_pending()
        time.sleep(60)
