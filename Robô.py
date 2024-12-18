from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import shutil
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Diretório onde os arquivos são baixados
download_dir = r"C:\Users\admin\Desktop\Dash Presidência - Teste"

# Lista de URLs ou ações para acessar e baixar cada arquivo
urls_com_filtro = [
    "https://redmine.prodesp.sp.gov.br/projects/portal-detran-sustentacao/issues?query_id=7701",
    "https://redmine.prodesp.sp.gov.br/projects/portal-detran-sustentacao/issues?query_id=7702",
    "https://redmine.prodesp.sp.gov.br/projects/suporte/issues?query_id=7699",
    "https://redmine.prodesp.sp.gov.br/projects/suporte/issues?query_id=7700"
]

# Nomes desejados para os arquivos baixados
nomes_arquivos = [
    "Portal Abertas - Presidência.xlsx",
    "Portal Concluídas - Presidência.xlsx",
    "Presidência - Abertas.xlsx",
    "Presidência - Concluídas.xlsx"
]

try:
    # Acessar a página de login
    url_login = "https://redmine.prodesp.sp.gov.br/login"
    driver.get(url_login)

    # Preencher o campo de login
    campo_usuario = driver.find_element(By.ID, "username")
    campo_usuario.send_keys("28875444897")

    # Preencher o campo de senha
    campo_senha = driver.find_element(By.ID, "password")
    campo_senha.send_keys("@15MN09cp77@")

    # Clicar no botão de login
    botao_login = driver.find_element(By.ID, "login-submit")
    botao_login.click()

    # Esperar o carregamento da página pós-login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))

    # Lista para armazenar DataFrames de cada arquivo
    dataframes = []

    # Loop para acessar cada URL e baixar os arquivos
    for i, url in enumerate(urls_com_filtro):
        driver.get(url)
        # Espera até o botão de download ser clicável
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='csv-export-form']/p[4]/input"))
        )
        download_button.click()

        # Aguardar o download
        time.sleep(10)

        # Nome do arquivo baixado automaticamente
        arquivo_baixado = os.path.join(download_dir, "issue.csv")

        # Verificar se o arquivo foi baixado e movê-lo para o diretório correto
        if os.path.exists(arquivo_baixado):
            novo_nome = os.path.join(download_dir, nomes_arquivos[i])
            shutil.move(arquivo_baixado, novo_nome)
            print(f"Arquivo renomeado para: {novo_nome}")
        else:
            print(f"Arquivo {arquivo_baixado} não encontrado. Verifique o processo de download.")

        # Carregar o arquivo renomeado no Pandas
        df = pd.read_csv(novo_nome, sep=';', encoding='latin-1')
        
        # Filtrar colunas (substitua pelos nomes das colunas desejadas)
        colunas_selecionadas = ['coluna1', 'coluna2', 'coluna3']  # Ajuste os nomes das colunas conforme necessário
        df_filtrado = df[colunas_selecionadas]

        # Adicionar o DataFrame filtrado à lista
        dataframes.append(df_filtrado)

    # Concatenar todos os DataFrames em um só
    df_consolidado = pd.concat(dataframes, ignore_index=True)

    # Salvar o DataFrame consolidado em uma nova planilha
    output_path = r"C:\Users\admin\Desktop\Dash Presidência - Teste\arquivo_consolidado.csv"
    df_consolidado.to_csv(output_path, index=False)

    print("Automação concluída com sucesso!")

except Exception as e:
    print("Ocorreu um erro:", e)

finally:
    driver.quit()  # Fechar o navegador após o processo
