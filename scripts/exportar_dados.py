import sqlite3
import pandas as pd

def exportar_clientes(conn, caminho_arquivo):
    query = """
        SELECT 
            c.razao_social AS "NOME",
            c.cpf_cnpj AS "CPF CNPJ",
            c.rg AS "RG",
            c.nacionalidade AS "NACIONALIDADE",
            c.nascimento AS "DATA DE NASCIMENTO",
            ec.descricao AS "ESTADO CIVIL",
            c.profissao AS "PROFISSÃO",
            NULL AS "SEXO", -- Valor padrão
            c.telefone2 AS "CELULAR",
            c.telefone1 AS "TELEFONE",
            c.email1 AS "EMAIL",
            NULL AS "PAIS", -- Valor padrão
            c.uf AS "ESTADO",
            c.cidade AS "CIDADE",
            c.bairro AS "BAIRRO",
            c.logradouro || ', ' || c.numero || ' ' || c.complemento AS "ENDEREÇO",
            c.cep AS "CEP",
            c.pis AS "PIS PASEP",
            NULL AS "CTPS", -- Valor padrão
            NULL AS "CID", -- Valor padrão
            c.nome_mae AS "NOME DA MÃE",
            'MIGRAÇÃO' AS "ORIGEM DO CLIENTE", -- Preenchimento padrão
            c.observacoes AS "ANOTAÇÕES GERAIS"
        FROM 
            clientes c
        LEFT JOIN 
            cliente_estado_civil ec ON c.cod_cliente_estado_civil = ec.codigo
        WHERE 
            c.ativo = 1;
    """
    df = pd.read_sql_query(query, conn)
    df.to_excel(caminho_arquivo, index=False, sheet_name="Clientes")

def exportar_processos(conn, caminho_arquivo):
    query = """
        SELECT 
            c.razao_social AS "NOME DO CLIENTE",
            (
                SELECT GROUP_CONCAT(pc.razao_social, '; ')
                FROM clientes pc
                JOIN litis_adverso la ON pc.codigo = la.cod_parte
                WHERE la.cod_processo = p.codigo
            ) AS "PARTE CONTRÁRIA",
            o.descricao AS "TIPO DE AÇÃO",
            gp.descricao AS "GRUPO DE AÇÃO",
            f.fase AS "FASE PROCESSUAL",
            p.numero_processo AS "NÚMERO DO PROCESSO",
            NULL AS "PROCESSO ORIGINÁRIO", -- Valor padrão
            tr.descricao AS "TRIBUNAL",
            NULL AS "VARA", -- Valor padrão
            cm.descricao AS "COMARCA",
            NULL AS "PROTOCOLO", -- Valor padrão
            p.valor_causa AS "EXPECTATIVA/VALOR DA CAUSA",
            NULL AS "VALOR HONORÁRIOS", -- Valor padrão
            NULL AS "PASTA", -- Valor padrão
            p.inclusao AS "DATA CADASTRO",
            p.data_encerramento AS "DATA FECHAMENTO",
            (
                SELECT MAX(r.data_julgamento) -- Substituição por coluna existente
                FROM recurso r
                WHERE r.codprocesso = p.codigo
            ) AS "DATA TRANSITO",
            NULL AS "DATA ARQUIVAMENTO", -- Valor padrão
            NULL AS "DATA REQUERIMENTO", -- Valor padrão
            NULL AS "RESPONSÁVEL", -- Valor padrão
            p.observacoes AS "ANOTAÇÕES GERAIS"
        FROM 
            processos p
        LEFT JOIN 
            clientes c ON p.cod_cliente = c.codigo
        LEFT JOIN 
            objeto_acao o ON p.objeto_acao = o.codigo
        LEFT JOIN 
            grupo_processo gp ON p.grupo_processo = gp.codigo
        LEFT JOIN 
            fase f ON p.codigo_fase = f.codigo
        LEFT JOIN 
            comarca cm ON p.codcomarca = cm.codigo
        LEFT JOIN 
            tribunal tr ON (
                SELECT r.codtribunal
                FROM recurso r
                WHERE r.codprocesso = p.codigo LIMIT 1
            ) = tr.codigo
        WHERE 
            p.ativo = 1;
    """
    df = pd.read_sql_query(query, conn)
    df.to_excel(caminho_arquivo, index=False, sheet_name="Processos")