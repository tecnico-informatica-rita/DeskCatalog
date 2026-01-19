def criar_view_produtos_emprestados_30_dias(conn):
    sql_select_view = """
    CREATE OR REPLACE VIEW visao_itens_para_devolucao_30_dias AS
    SELECT 
    n.nome_produto,
    e.nome_emprestimos,
    e.id_disponibilidade,  
    TO_CHAR(e.data_emprestimo, 'DD/MM/YYYY') AS data_brasil,
    COUNT(e.nu_patrimonio) AS quantidade_emprestada,
    s.descricao_disponibilidade  
    FROM 
    emprestimos AS e
    JOIN 
    produtos_individuais AS pi ON pi.nu_patrimonio = e.nu_patrimonio
    JOIN 
    nomes_produtos AS n ON n.id_produto = pi.id_produto
    JOIN 
    status_disponibilidade_produto AS s ON s.id_disponibilidade = e.id_disponibilidade
    WHERE
    s.descricao_disponibilidade = 'Em atraso'
    OR (s.descricao_disponibilidade = 'Emprestado' 
        AND e.data_emprestimo >= (CURRENT_DATE - INTERVAL '30 days'))
    GROUP BY 
    n.nome_produto, 
    e.nome_emprestimos, 
    e.data_emprestimo,
    e.id_disponibilidade,
    s.descricao_disponibilidade
    ORDER BY 
    e.data_emprestimo DESC;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql_select_view,)
            print("View criada")
        return True
    except Exception as e:
        raise ValueError (f"Erro inesperado ao realizar query: {e}")
    

def criar_view_historico_emprestados(conn):
    sql_select_view = """
        CREATE OR REPLACE VIEW visao_historico_transacoes_emprestimos AS
        SELECT n.nome_produto, e.nome_emprestimos, e.data_emprestimo, s.descricao_disponibilidade, COUNT(e.nu_patrimonio) AS quantidade_total
        FROM emprestimos AS e
        JOIN produtos_individuais AS pi ON pi.nu_patrimonio = e.nu_patrimonio
        JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
        JOIN status_disponibilidade_produto AS s ON s.id_disponibilidade = e.id_disponibilidade
        GROUP BY n.nome_produto, e.nome_emprestimos, e.data_emprestimo, s.descricao_disponibilidade 
        ORDER BY 
        e.data_emprestimo DESC;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql_select_view,)
            print("View criada")
        return True
    except Exception as e:
        raise ValueError (f"Erro inesperado ao realizar query: {e}")



