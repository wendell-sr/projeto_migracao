import sqlite3
import json

# Substitua pelo caminho do seu arquivo de banco de dados SQLite
caminho_banco = 'data/database.sqlite'

# Conecta ao banco de dados SQLite
conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

# Obtém a lista de tabelas disponíveis
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = [tabela[0] for tabela in cursor.fetchall()]

informacoes_banco = {}

for nome_tabela in tabelas:
    # Obtém as colunas da tabela atual
    cursor.execute(f'PRAGMA table_info("{nome_tabela}")')
    colunas_info = cursor.fetchall()
    info_colunas = {}
    for coluna in colunas_info:
        nome_coluna = coluna[1]
        tipo_coluna = coluna[2]
        # Obtém o primeiro valor da coluna como exemplo
        cursor.execute(f'SELECT "{nome_coluna}" FROM "{nome_tabela}" LIMIT 1')
        resultado = cursor.fetchone()
        valor_exemplo = resultado[0] if resultado else None
        info_colunas[nome_coluna] = {
            'tipo': tipo_coluna,
            'exemplo': valor_exemplo
        }
    informacoes_banco[nome_tabela] = info_colunas

# Fecha a conexão com o banco de dados
conexao.close()

# Converte o dicionário para JSON e salva em um arquivo
with open('informacoes_banco.json', 'w', encoding='utf-8') as f:
    json.dump(informacoes_banco, f, indent=4, ensure_ascii=False, default=str)

print("Arquivo 'informacoes_banco.json' gerado com sucesso!")
