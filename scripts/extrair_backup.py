import os
import sqlite3
import pandas as pd
import py7zr
import patoolib

def limpar_nome_tabela(nome_arquivo):
    """
    Limpa o nome do arquivo para usá-lo como nome da tabela.
    Remove 'v_' no início e '_CodEmpresa_92577' no final.
    """
    tabela = nome_arquivo
    if tabela.startswith("v_"):
        tabela = tabela[2:]  # Remove o prefixo 'v_'
    if tabela.endswith("_CodEmpresa_92577.csv"):
        tabela = tabela.replace("_CodEmpresa_92577.csv", "")  # Remove o sufixo e extensão
    elif tabela.endswith("_CodEmpresa_92577"):
        tabela = tabela.replace("_CodEmpresa_92577", "")  # Remove o sufixo
    tabela = tabela.replace(".csv", "")  # Remove a extensão (caso ainda exista)
    return tabela

def criar_banco(diretorio_csv="data/input", caminho_banco="data/database.sqlite"):
    """
    Cria um banco de dados SQLite e popula com os dados dos arquivos CSV usando UTF-8.
    Sobrescreve o banco de dados existente.
    """
    # Remover o banco de dados antigo, se existir
    if os.path.exists(caminho_banco):
        os.remove(caminho_banco)
        print(f"Banco de dados antigo '{caminho_banco}' removido.")

    conn = sqlite3.connect(caminho_banco)
    arquivos_csv = [f for f in os.listdir(diretorio_csv) if f.endswith(".csv")]

    for arquivo in arquivos_csv:
        tabela = limpar_nome_tabela(arquivo)
        caminho_arquivo = os.path.join(diretorio_csv, arquivo)
        try:
            print(f"Processando {arquivo} como tabela '{tabela}'...")
            df = pd.read_csv(caminho_arquivo, encoding="utf-8", delimiter=";")
            df.to_sql(tabela, conn, if_exists="replace", index=False)
            print(f"Tabela '{tabela}' criada com sucesso.")
        except UnicodeDecodeError as e:
            print(f"Erro de codificação ao processar '{arquivo}': {e}. Tentando com 'latin-1'.")
            try:
                df = pd.read_csv(caminho_arquivo, encoding="latin-1", delimiter=";")
                df.to_sql(tabela, conn, if_exists="replace", index=False)
                print(f"Tabela '{tabela}' criada com sucesso com 'latin-1'.")
            except Exception as ex:
                print(f"Erro ao processar o arquivo '{arquivo}' com 'latin-1': {ex}")
        except Exception as e:
            print(f"Erro ao processar o arquivo '{arquivo}': {e}")

    conn.commit()
    conn.close()

def extrair_backup(caminho_backup, diretorio_saida):
    """
    Extrai arquivos de um backup compactado e cria o banco de dados.
    """
    # Limpar diretório de saída antes de extrair os arquivos
    if os.path.exists(diretorio_saida):
        for arquivo in os.listdir(diretorio_saida):
            caminho = os.path.join(diretorio_saida, arquivo)
            if os.path.isfile(caminho):
                os.remove(caminho)
            elif os.path.isdir(caminho):
                os.rmdir(caminho)
        print(f"Diretório '{diretorio_saida}' limpo.")

    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)

    if caminho_backup.endswith(".rar"):
        patoolib.extract_archive(caminho_backup, outdir=diretorio_saida)
    elif caminho_backup.endswith(".7z"):
        with py7zr.SevenZipFile(caminho_backup, mode="r") as z:
            z.extractall(path=diretorio_saida)

    criar_banco(diretorio_saida)
