import os
import pandas as pd
import chardet

def detectar_codificacao(caminho):
    """Detecta a codificação de um arquivo."""
    with open(caminho, "rb") as f:
        result = chardet.detect(f.read())
        return result["encoding"]

def tratar_arquivo(input_path, output_path, tratamento):
    """
    Carrega, trata e salva os dados de um arquivo CSV.

    Args:
        input_path (str): Caminho do arquivo de entrada.
        output_path (str): Caminho do arquivo de saída.
        tratamento (function): Função de tratamento aplicada aos dados.
    """
    try:
        # Detectar a codificação do arquivo
        encoding = detectar_codificacao(input_path)
        print(f"Codificação detectada: {encoding}")

        # Carregar o arquivo
        df = pd.read_csv(input_path, encoding=encoding, delimiter=";")

        # Aplicar o tratamento
        df_tratado = tratamento(df)

        # Salvar o arquivo tratado
        df_tratado.to_csv(output_path, index=False, encoding="utf-8")
        print(f"Arquivo tratado salvo em: {output_path}")
    except Exception as e:
        print(f"Erro ao processar o arquivo {input_path}: {e}")

def tratar_clientes(df):
    """Aplica os tratamentos específicos para o arquivo de clientes."""
    if "nome" in df.columns:
        df["nome"] = df["nome"].fillna("Não Informado").str.title()
    return df

def tratar_processos(df):
    """Aplica os tratamentos específicos para o arquivo de processos."""
    if "numero_processo" in df.columns:
        df["numero_processo"] = df["numero_processo"].fillna("Não Informado")
    return df

if __name__ == "__main__":
    # Diretórios de entrada e saída
    input_dir = "data/input"
    output_dir = "data/output"

    # Tratar arquivo de clientes
    tratar_arquivo(
        input_path=os.path.join(input_dir, "v_clientes_CodEmpresa_92577.csv"),
        output_path=os.path.join(output_dir, "clientes_tratados.csv"),
        tratamento=tratar_clientes,
    )

    # Tratar arquivo de processos
    tratar_arquivo(
        input_path=os.path.join(input_dir, "v_processos_CodEmpresa_92577.csv"),
        output_path=os.path.join(output_dir, "processos_tratados.csv"),
        tratamento=tratar_processos,
    )
