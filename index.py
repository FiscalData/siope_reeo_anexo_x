import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def carregar_api_key(caminho_arquivo):
    """
    Lê a API_KEY de um arquivo de texto.

    Args:
        caminho_arquivo (str): Caminho do arquivo contendo a API_KEY.

    Returns:
        str: A chave da API.
    """
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            api_key = arquivo.read().strip()
        return api_key
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo {caminho_arquivo} não foi encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")


# Função para resolver o reCAPTCHA
def resolver_recaptcha(driver, API_KEY, site_key, resolved_tokens):
    url = driver.current_url
    # Se o token já foi resolvido para essa página, reutilize-o
    if url in resolved_tokens:
        print("Usando token de reCAPTCHA já resolvido.")
        return resolved_tokens[url]
    
    response = requests.get(
        f"http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={site_key}&pageurl={url}")
    
    if '|' not in response.text:
        print(f"Erro ao solicitar resolução do CAPTCHA: {response.text}")
        return None

    captcha_id = response.text.split('|')[1]

    for attempt in range(20):
        time.sleep(5)
        print(f"Requisição #{attempt + 1} para obter resposta do CAPTCHA...")
        captcha_response = requests.get(f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}")

        if '|' in captcha_response.text:
            recaptcha_token = captcha_response.text.split('|')[1]
            resolved_tokens[url] = recaptcha_token  # Armazena o token resolvido
            return recaptcha_token
        elif captcha_response.text != "CAPCHA_NOT_READY":
            print(f"Erro ao obter resposta do CAPTCHA: {captcha_response.text}")
            return None

    print("O CAPTCHA não foi resolvido a tempo.")
    return None

# Função para verificar se o PDF já foi baixado
def verificar_pdf_baixado(municipio_code):
    downloads_dir = r"C:\Users\z3tsu\Downloads"
    for file_name in os.listdir(downloads_dir):
        if file_name.endswith(".pdf") and municipio_code in file_name:
            return True
    return False

# Função para verificar e registrar tentativa
def verificar_e_registrar_tentativa(municipio_code):
    log_path = "municipios_tentados.txt"
    
    if os.path.exists(log_path):
        with open(log_path, 'r') as log_file:
            municipios_tentados = log_file.read().splitlines()
    else:
        municipios_tentados = []

    if municipio_code in municipios_tentados:
        return True
    
    with open(log_path, 'a') as log_file:
        log_file.write(f"{municipio_code}\n")
    
    return False

# Configuração do Selenium
def iniciar_driver():
    driver = webdriver.Chrome()
    driver.get("https://www.fnde.gov.br/siope/relatorioRREOMunicipal2006.do")
    return driver

# Função para baixar o PDF
def baixar_pdf_por_municipio(driver, API_KEY, site_key, estado, cidade, resolved_tokens):
    try:
        select_cidade = Select(driver.find_element("name", "municipios"))
        select_cidade.select_by_value(cidade)

        recaptcha_token = resolver_recaptcha(driver, API_KEY, site_key, resolved_tokens)
        if recaptcha_token is None:
            print(f"Falha ao resolver o CAPTCHA para o município {cidade}, tentando novamente...")
            return False

        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_token}";')

        driver.find_element("name", "Submit").click()
        time.sleep(1)
        driver.back()
        time.sleep(3)
        
        return True

    except Exception as e:
        print(f"Erro ao baixar PDF para município {cidade}: {e}")
        return False

# Função principal
def executar_processo_download(API_KEY, site_key, estados):
    resolved_tokens = {}  # Dicionário para armazenar tokens já resolvidos
    while True:
        driver = iniciar_driver()
        select_anos = Select(driver.find_element("name", "anos"))
        select_anos.select_by_value("2023")

        for estado in estados:
            select_estado = Select(driver.find_element("name", "cod_uf"))
            select_estado.select_by_value(estado)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "municipios"))
            )
            select_cidade = Select(driver.find_element("name", "municipios"))
            municipios = [option.get_attribute("value") for option in select_cidade.options if option.get_attribute("value") != '']

            for cidade in municipios:
                if verificar_pdf_baixado(cidade) or verificar_e_registrar_tentativa(cidade):
                    print(f"PDF ou tentativa para o município {cidade} já existe, pulando...")
                    continue

                sucesso = baixar_pdf_por_municipio(driver, API_KEY, site_key, estado, cidade, resolved_tokens)
                if not sucesso:
                    print("Reiniciando o processo devido a um erro...")
                    driver.quit()
                    time.sleep(25)
                    break

        driver.quit()


# Substitua pelo caminho do arquivo que contém a API_KEY
caminho_arquivo = 'api_key.txt'

try:
    API_KEY = carregar_api_key(caminho_arquivo)
    print(f"API_KEY carregada: {API_KEY}")
except Exception as e:
    print(e)

site_key = '6Lc1KqcUAAAAACYWpPxX2r3E6aTSyZDos0hT1uh3'
estados = ["12", "27", "16", "13", "29", "23", "32", "52", "21", "51", "50", "31", "15", "25", "41", "26", "22", "33", "24", "43", "11", "14", "42", "35", "28", "17"]

executar_processo_download(API_KEY, site_key, estados)
