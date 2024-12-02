import pandas as pd

def exportar_clientes(conn, caminho_arquivo):
    query = """
        SELECT
            c.razao_social AS NOME,
            c.cpf_cnpj AS "CPF CNPJ",
            c.rg AS RG,
            c.nacionalidade AS NACIONALIDADE,
            c.nascimento AS "DATA DE NASCIMENTO",
            c.estado_civil AS "ESTADO CIVIL",
            c.profissao AS PROFISSÃO,
            c.telefone1 AS CELULAR,
            c.telefone2 AS TELEFONE,
            c.cidade AS CIDADE,
            c.bairro AS BAIRRO,
            c.logradouro AS ENDEREÇO,
            c.cep AS CEP,
            c.pis AS "PIS PASEP",
            c.nome_mae AS "NOME DA MÃE",
            c.observacoes AS "ANOTAÇÕES GERAIS"
        FROM clientes c
        LEFT JOIN estado_brasil e ON c.cod_estado_brasil = e.codigo;

    """
    df = pd.read_sql_query(query, conn)
    df.to_excel(caminho_arquivo, index=False, sheet_name="Clientes")

def exportar_processos(conn, caminho_arquivo):
    query = """
        SELECT
            c.razao_social AS "NOME DO CLIENTE",
            p.numero_processo AS "NÚMERO DO PROCESSO",
            p.tipo_acao AS "TIPO DE AÇÃO",
            g.descricao AS "GRUPO DE AÇÃO",
            co.descricao AS COMARCA,
            p.valor_causa AS "EXPECTATIVA/VALOR DA CAUSA",
            p.pasta AS PASTA,
            p.inclusao AS "DATA CADASTRO",
            p.data_transitojulgado AS "DATA TRANSITO",
            u.nome AS RESPONSÁVEL,
            p.observacoes AS "ANOTAÇÕES GERAIS"
        FROM processos p
        LEFT JOIN clientes c ON p.cod_cliente = c.codigo
        LEFT JOIN grupo_processo g ON p.grupo_processo = g.codigo
        LEFT JOIN comarca co ON p.codcomarca = co.codigo
        LEFT JOIN usuario u ON p.cod_usuario = u.id;

    """
    df = pd.read_sql_query(query, conn)
    df.to_excel(caminho_arquivo, index=False, sheet_name="Processos")
