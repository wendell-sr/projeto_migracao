import pandas as pd

def exportar_clientes(conn, caminho_arquivo):
    query = """
            SELECT 
                COALESCE(c.razao_social, '') AS NOME,
                COALESCE(c.cpf, '') AS "CPF CNPJ",
                COALESCE(c.rg, '') AS RG,
                COALESCE(c.nacionalidade, '') AS NACIONALIDADE,
                COALESCE(c.nascimento, '') AS "DATA DE NASCIMENTO",
                COALESCE(ec.descricao, '') AS "ESTADO CIVIL",
                COALESCE(c.profissao, '') AS PROFISSÃO,
                '' AS SEXO, -- Não mapeado no banco
                COALESCE(c.telefone2, '') AS CELULAR,
                COALESCE(c.telefone1, '') AS TELEFONE,
                COALESCE(c.email1, '') AS EMAIL,
                '' AS PAIS, -- Não mapeado no banco
                COALESCE(c.uf, '') AS ESTADO,
                COALESCE(c.cidade, '') AS CIDADE,
                COALESCE(c.bairro, '') AS BAIRRO,
                COALESCE(c.logradouro || ', ' || COALESCE(c.numero, '') || ' ' || COALESCE(c.complemento, ''), '') AS ENDEREÇO,
                COALESCE(c.cep, '') AS CEP,
                '' AS "PIS PASEP", -- Não mapeado no banco
                '' AS CTPS, -- Não mapeado no banco
                '' AS CID, -- Não mapeado no banco
                COALESCE(c.nome_mae, '') AS "NOME DA MÃE",
                '' AS "ORIGEM DO CLIENTE", -- Não mapeado no banco
                COALESCE(c.observacoes, '') AS "ANOTAÇÕES GERAIS"
            FROM 
                clientes c
            LEFT JOIN 
                cliente_estado_civil ec ON c.estado_civil = ec.codigo
            WHERE 
                c.ativo = 1;

    """
    df = pd.read_sql_query(query, conn)
    df.to_excel(caminho_arquivo, index=False, sheet_name="Clientes")


def exportar_processos(conn, caminho_arquivo):
    query = """ 
        SELECT 
            COALESCE(c.razao_social, '') AS "NOME DO CLIENTE",
            (
                SELECT GROUP_CONCAT(pc.razao_social, '; ')
                FROM clientes pc
                JOIN litis_adverso la ON pc.codigo = la.cod_parte
                WHERE la.cod_processo = p.codigo
            ) AS "PARTE CONTRÁRIA",
            COALESCE(o.descricao, '') AS "TIPO DE AÇÃO",
            COALESCE(g.descricao, '') AS "GRUPO DE AÇÃO",
            COALESCE(f.fase, '') AS "FASE PROCESSUAL",
            COALESCE(p.numero_processo, '') AS "NÚMERO DO PROCESSO",
            '' AS "PROCESSO ORIGINÁRIO", -- Não mapeado no banco
            (
                SELECT t.descricao
                FROM tribunal t
                WHERE t.codigo = (
                    SELECT tr.codigo
                    FROM recurso tr
                    WHERE tr.codprocesso = p.codigo
                    LIMIT 1
                )
            ) AS TRIBUNAL,
            '' AS VARA, -- Não especificado
            COALESCE(cm.descricao, '') AS COMARCA,
            '' AS PROTOCOLO, -- Não especificado
            COALESCE(p.valor_causa, 0.0) AS "EXPECTATIVA/VALOR DA CAUSA",
            '' AS "VALOR HONORÁRIOS", -- Não mapeado no banco
            '' AS PASTA, -- Não mapeado no banco
            COALESCE(p.inclusao, '') AS "DATA CADASTRO",
            COALESCE(p.data_encerramento, '') AS "DATA FECHAMENTO",
            (
                SELECT MAX(data_transitojulgado)
                FROM processos
                WHERE codigo = p.codigo
            ) AS "DATA TRANSITO",
            '' AS "DATA ARQUIVAMENTO", -- Não mapeado no banco
            '' AS "DATA REQUERIMENTO", -- Não mapeado no banco
            '' AS RESPONSÁVEL, -- Não mapeado no banco
            COALESCE(p.observacoes, '') AS "ANOTAÇÕES GERAIS"
        FROM 
            processos p
        LEFT JOIN 
            clientes c ON p.cod_cliente = c.codigo
        LEFT JOIN 
            fase f ON p.codigo_fase = f.codigo
        LEFT JOIN 
            comarca cm ON p.codcomarca = cm.codigo
        LEFT JOIN 
            objeto_acao o ON p.objeto_acao = o.codigo
        LEFT JOIN 
            grupo_processo g ON p.grupo_processo = g.codigo
        WHERE 
            p.ativo = 1;

    """
    df = pd.read_sql_query(query, conn)
    df.to_excel(caminho_arquivo, index=False, sheet_name="Processos")

