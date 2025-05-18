from datetime import datetime
import os
import sys
import html2text

def caminho_relativo(nome_arquivo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'corpo_email', nome_arquivo)
    return os.path.join('corpo_email', nome_arquivo)


def comprimento():
    hoje = datetime.now()
    hora = hoje.hour
    data_str = hoje.strftime('%d/%m/%Y')

    if  00 <= hora < 12:
        saudacao = "Bom dia" 
    elif 12<= hora < 18:
        saudacao = "Boa tarde"
    elif 18<= hora < 23:
        saudacao = "Boa Noite"

    return data_str, saudacao


def email(alertas):
    tamanho = str(len(alertas))
    data_str, saudacao = comprimento()

    caminho_html = caminho_relativo('mensagem/email_comp.html')

    with open(file=caminho_html, mode='r', encoding='utf-8') as html:
        html_comp = html.read()

    html_comp = html_comp.replace('{{saudacao}}', saudacao)
    html_comp = html_comp.replace('{{resultado}}', tamanho)
    html_comp = html_comp.replace('{{hoje}}', data_str)

    tabela_html = ""
    for alerta in alertas:
        fabricante = alerta['fabricante']
        titulo = alerta['titulo']
        urgencia = alerta['urgencia']
        link = alerta['link']
        tabela_html += f"""
                    <tr>
                        <td>{fabricante}</td>
                        <td>{titulo}</td>
                        <td>{urgencia}</td>
                        <td>{link}</td>
                    </tr>
                    """
    html_comp = html_comp.replace('{{tabela_alertas}}', tabela_html)
    
    #print(html_comp)
    return html_comp

#html('10')


def teams(alertas):
    tamanho = str(len(alertas))
    data_str, saudacao = comprimento()

    caminho_html = caminho_relativo('mensagem/teams.html')

    with open(file=caminho_html, mode='r', encoding='utf-8') as html:
        html_comp = html.read()

    html_comp = html_comp.replace('{{saudacao}}', saudacao)
    html_comp = html_comp.replace('{{resultado}}', tamanho)
    html_comp = html_comp.replace('{{hoje}}', data_str)

    tabela_html = ""
    for alerta in alertas:
        fabricante = alerta['fabricante']
        titulo = alerta['titulo']
        urgencia = alerta['urgencia']
        link = alerta['link']

        tabela_html += f"""
            <tr>
                <td style="padding:5px; border:1px solid #ccc;">{fabricante}</td>
                <td style="padding:5px; border:1px solid #ccc;">{titulo}</td>
                <td style="padding:5px; border:1px solid #ccc;">{urgencia}</td>
                <td style="padding:5px; border:1px solid #ccc;">
                    <a href="{link}" target="_blank">{link}</a>
                </td>
            </tr>
        """

    html_comp = html_comp.replace('{{tabela_alertas}}', tabela_html)
    
    h = html2text.HTML2Text()
    # Ignore converting links from HTML
    h.ignore_links = False
    markdown = h.handle(html_comp)
    
    #print(html_comp)
    return markdown

#teams()
