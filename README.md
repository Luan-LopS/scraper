# 🕷️ CVE Scraper - Monitoramento Automático de Vulnerabilidades

## Descrição

Este projeto realiza **web scraping de CVEs (Common Vulnerabilities and Exposures)** em **17 sites diferentes**, com foco em **monitoramento automatizado de vulnerabilidades de segurança**. A aplicação executa as tarefas em **paralelo**, garantindo eficiência e velocidade na coleta dos dados.

Após a coleta, os dados são:

- Organizados e salvos em um **arquivo Excel**.
- Enviados por **email** para os destinatários cadastrados.
- Notificados via **Microsoft Teams**, informando sobre novas ocorrências encontradas.

O sistema é configurado para rodar de forma **automática a cada 4 horas** através de um **agendador de tarefas (scheduler)**. O projeto será distribuído como um **executável standalone**, facilitando sua execução em ambientes que não possuem dependências pré-instaladas.

---

## Funcionalidades

- 🔍 Scraping de CVEs em 17 fontes confiáveis
- ⚙️ Execução paralela para maior performance
- 📊 Geração de relatório em formato Excel
- 📧 Envio automático por email
- 💬 Notificações automáticas no Microsoft Teams
- ⏱️ Agendamento de execução a cada 4 horas
- 🛠️ Empacotado como executável para fácil distribuição

---

## Requisitos

- Python 3.8+
- Bibliotecas:
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `smtplib` / `email`
  - `schedule` ou `APScheduler`
  - `concurrent.futures`
  - Outros conforme dependências específicas

---

## Como usar

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/cve-scraper.git
cd cve-scraper
