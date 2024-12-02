import pandas as pd

def exportar_clientes(conn, caminho_arquivo):
    query = """
        SELECT
            c.codigo AS cliente_id,
            c.razao_social AS nome_cliente,
            c.cpf_cnpj AS cpf,
            c.email1 AS email,
            e.uf AS estado_cliente,
            g.descricao AS grupo_cliente
        FROM clientes c
        LEFT JOIN grupo_cliente g ON c.grupo_cliente = g.codigo
        LEFT JOIN estado_brasil e ON c.cod_estado_brasil = e.codigo;
    """
    df = pd.read_sql_query(query, conn)
    df.to_excel(caminho_arquivo, index=False, sheet_name="Clientes")

def exportar_processos(conn, caminho_arquivo):
    query = """
        SELECT
            p.codigo AS processo_id,
            p.numero_processo AS numero,
            p.data_distribuicao AS data_inicio,
            c.razao_social AS cliente,
            p.uf AS estado_processo,
            g.descricao AS grupo_processo
        FROM processos p
        LEFT JOIN clientes c ON p.cod_cliente = c.codigo
        LEFT JOIN grupo_processo g ON p.grupo_processo = g.codigo;
    """
    df = pd.read_sql_query(query, conn)
    df.to_excel(caminho_arquivo, index=False, sheet_name="Processos")
