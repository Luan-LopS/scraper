from datetime import datetime
import os
import sys

def caminho_relativo(nome_arquivo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'corpo_email', nome_arquivo)
    return os.path.join('corpo_email', nome_arquivo)

def html(tamanho):
    hoje = datetime.now()
    hora = hoje.hour
    data_str = hoje.strftime('%d/%m/%Y')

    if  00 <= hora < 12:
        saudacao = "Bom dia" 
    elif 12<= hora < 18:
        saudacao = "Boa tarde"
    elif 18<= hora < 23:
        saudacao = "Boa Noite"

    caminho_html = caminho_relativo('email_comp.html')


    with open(file=caminho_html, mode='r', encoding='utf-8') as html:
        html_comp = html.read()

    html_comp = html_comp.replace('{{saudacao}}', saudacao)
    html_comp = html_comp.replace('{{resultado}}', tamanho)
    html_comp = html_comp.replace('{{hoje}}', data_str)

    #print(html_comp)
    return html_comp

#html('10')