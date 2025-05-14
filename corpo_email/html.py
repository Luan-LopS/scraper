from datetime import datetime

def html(tamanho):
    hoje = datetime.now()
    hora = hoje.hour
    data_str = hoje.strftime('%d/%m/%Y')

    if  00 <= hora < 12:
        saudacao = "Bom dia" 
    elif 12<= hora < 18:
        saudacao = "Boa tarde"
    elif 18<= hora < 00:
        saudacao = "Boa Noite"

    with open(file='corpo_email/email_comp.html', mode='r', encoding='utf-8') as html:
        html_comp = html.read()

    html_comp = html_comp.replace('{{saudacao}}', saudacao)
    html_comp = html_comp.replace('{{resultado}}', tamanho)
    html_comp = html_comp.replace('{{hoje}}', data_str)

    #print(html_comp)
    return html_comp

#html('10')