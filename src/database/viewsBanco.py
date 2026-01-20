# tabelas criadas no banco para facilitar consultas

# ===========================================================================================================================
# ======================================== PARTE DA RITA =====================================================================
# ===========================================================================================================================

def criar_view_todos_produtos(conn): # consertar para transformar ela em histórico
    sql_select_view = """
        CREATE OR REPLACE VIEW vw_todos_produtos AS
        SELECT pi.nu_patrimonio, c.nome_categoria, n.nome_produto, s.descricao_status
        FROM produtos_individuais AS pi 
        JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
        JOIN categorias_produto AS c ON c.id_categoria = n.id_categoria

        JOIN status_produto AS s ON s.id_status_produto = pi.id_status_produto

        ORDER BY 
        c.nome_categoria ASC,
        n.nome_produto ASC,
        pi.nu_patrimonio DESC
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql_select_view,)
        return True
    except Exception as e:
        raise ValueError (f"Erro inesperado ao realizar query: {e}")
    
def criar_view_produtos_exibicao_qtdAtivos(conn):
    sql_select_view = """
        CREATE OR REPLACE VIEW vw_todos_produtos_qtdAtivos AS
        SELECT c.nome_categoria, n.nome_produto, 
		COUNT(pi.id_produto) AS total_produtos, 
		COUNT(CASE WHEN s.descricao_status = 'Ativo' THEN 1 END) AS total_prod_ativos
        FROM produtos_individuais AS pi 
        JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
        JOIN categorias_produto AS c ON c.id_categoria = n.id_categoria
		JOIN status_produto AS s ON pi.id_status_produto = s.id_status_produto
		GROUP BY c.nome_categoria, n.nome_produto
        ORDER BY 
        c.nome_categoria ASC,
        n.nome_produto ASC;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql_select_view,)
        return True
    except Exception as e:
        raise ValueError (f"Erro inesperado ao realizar query: {e}")
    
def criar_view_prod_disponiveis(conn):
    sql_select_view = """
        CREATE OR REPLACE VIEW vw_produtos_disponiveis AS
        SELECT 
        c.nome_categoria,
        n.nome_produto,
        COUNT(pi.nu_patrimonio) AS total_produtos,
        COALESCE(SUM(
            CASE 
                WHEN s.descricao_status = 'Ativo' 
                    AND NOT EXISTS (
                        SELECT 1
                        FROM emprestimos e2
                        JOIN status_disponibilidade_produto sdp 
                        ON e2.id_disponibilidade = sdp.id_disponibilidade
                        WHERE e2.nu_patrimonio = pi.nu_patrimonio
                        AND sdp.descricao_disponibilidade = 'Emprestado'
                    )
                THEN 1 
                ELSE 0 
            END
        ), 0) AS total_disponiveis
    FROM categorias_produto AS c
    INNER JOIN nomes_produtos AS n ON n.id_categoria = c.id_categoria
    INNER JOIN produtos_individuais AS pi ON pi.id_produto = n.id_produto
    INNER JOIN status_produto AS s ON s.id_status_produto = pi.id_status_produto
    GROUP BY c.nome_categoria, n.nome_produto
    ORDER BY c.nome_categoria, n.nome_produto;

    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql_select_view,)
            return True
    except Exception as e:
        raise ValueError (f"Erro inesperado ao realizar query: {e}")
    
def view_grafico_comparacao_ativos_inativos(conn):
        sql_select_view = """
        CREATE OR REPLACE VIEW vw_grafico_AtivoInativo AS
        SELECT 
            SUM(CASE WHEN s.descricao_status = 'Ativo' THEN 1 END) AS produtos_ativos,
		    SUM(CASE WHEN s.descricao_status <> 'Ativo' THEN 1 END) AS produtos_inativos,
            FROM produtos_individuais AS pi
            JOIN status_produto AS s ON pi.id_status_produto = s.id_status_produto
    """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")

def view_grafico_emprestimoCat_diarios(conn):
        sql_select_view = """
        CREATE OR REPLACE VIEW vw_grafico_empCatDia AS
        SELECT c.nome_categoria, COUNT(*) AS emprestimos_ativos
        FROM emprestimos AS e
        JOIN produtos_individuais AS pi ON pi.nu_patrimonio = e.nu_patrimonio
        JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
        JOIN categorias_produto AS c ON c.id_categoria = n.id_categoria
        WHERE CURRENT_DATE BETWEEN e.data_emprestimo AND e.data_devolucao
        GROUP BY c.nome_categoria
        ORDER BY emprestimos_ativos DESC;
    """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def view_grafico_itensPenCat(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW vw_grafico_itensPenCat AS
            SELECT c.nome_categoria, COUNT(*) AS itens_pendentes
            FROM categorias_produto c
            LEFT JOIN nomes_produtos n ON n.id_categoria = c.id_categoria
            LEFT JOIN produtos_individuais pi ON pi.id_produto = n.id_produto
            LEFT JOIN emprestimos e ON e.nu_patrimonio = pi.nu_patrimonio
            WHERE e.data_devolucao < CURRENT_DATE AND e.devolvido_em IS NULL
            GROUP BY c.nome_categoria
            ORDER BY c.nome_categoria;
    """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_produtos_emprestados_30_dias(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW vw_itens_para_devolucao_30 AS
            SELECT n.nome_produto, e.nome_emprestimos, TO_CHAR(e.data_emprestimo, 'DD/MM/YYYY') AS data_brasil, COUNT(e.nu_patrimonio) AS quantidade_emprestada
            FROM emprestimos AS e
            JOIN produtos_individuais AS pi ON pi.nu_patrimonio = e.nu_patrimonio
            JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
            JOIN status_disponibilidade_produto AS s ON s.id_disponibilidade = e.id_disponibilidade
            WHERE
                s.descricao_disponibilidade = 'Em atraso' 
                OR (s.descricao_disponibilidade = 'Emprestado' AND e.data_emprestimo >= (CURRENT_DATE - INTERVAL '30 days'))
            GROUP BY n.nome_produto, e.nome_emprestimos, e.data_emprestimo
            ORDER BY e.data_emprestimo DESC;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_devolucoes(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW vw_devolucoes AS
            SELECT 
	        c.nome_categoria,
            n.nome_produto,
            e.nome_emprestimos AS pessoa,
            TO_CHAR(e.data_emprestimo, 'DD/MM/YYYY') AS data_emprestimo,
            s.descricao_disponibilidade,
            COUNT(*) AS quantidade_total
            FROM emprestimos AS e
            JOIN produtos_individuais AS pi ON pi.nu_patrimonio = e.nu_patrimonio
            JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
            JOIN categorias_produto AS c ON c.id_categoria = n.id_categoria
            JOIN status_disponibilidade_produto AS s ON s.id_disponibilidade = e.id_disponibilidade
            WHERE s.descricao_disponibilidade IN ('Emprestado', 'Em atraso')
            GROUP BY 
	        c.nome_categoria,
            n.nome_produto,
            e.nome_emprestimos,
            TO_CHAR(e.data_emprestimo, 'DD/MM/YYYY'),
            s.descricao_disponibilidade
            ORDER BY 
            MAX(e.data_emprestimo) DESC;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")

# ===========================================================================================================================
# ======================================== PARTE DA ANA =====================================================================
# ===========================================================================================================================

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
    

#   ================ CRIAÇÃO DAS VIEWS ===========================
        
def criar_todas_views(conn):
    criar_view_produtos_exibicao_qtdAtivos(conn)
    criar_view_todos_produtos(conn)
    view_grafico_comparacao_ativos_inativos(conn)
    view_grafico_emprestimoCat_diarios(conn)
    view_grafico_itensPenCat(conn)
    criar_view_prod_disponiveis(conn)
    criar_view_produtos_emprestados_30_dias(conn)
    criar_view_devolucoes(conn)




