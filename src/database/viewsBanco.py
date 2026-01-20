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
        pi.nu_patrimonio DESC;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql_select_view,)
        return True
    except Exception as e:
        raise ValueError (f"Erro inesperado ao realizar query de todos os produtos: {e}")
    
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
        raise ValueError (f"Erro inesperado ao realizar query da exibição de produtos ativos: {e}")
    
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
            COUNT(*) AS total
            FROM produtos_individuais AS pi
            JOIN status_produto AS s ON pi.id_status_produto = s.id_status_produto;
    """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query de produtos ativos X inativos: {e}")

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

def criar_view_visao_audio_e_video(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_audio_e_video AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Áudio e Vídeo'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_eletrodomesticos(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_eletrodomesticos
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Eletrodomésticos'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_equipamentos_eletronicos(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_equipamentos_eletronicos
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Equipamentos Eletrônicos'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_esportes_e_lazer(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_esportes_e_lazer
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Esportes e Lazer'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_esportes_e_lazer(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_esportes_e_lazer
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Esportes e Lazer'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_historico_transacoes_emprestimos(conn):
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
    
def criar_view_visao_informatica(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_informatica
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Informática'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_infraestrutura(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_infraestrutura
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Infraestrutura'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_itens_para_devolucao_30_dias(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_itens_para_devolucao_30_dias
            AS SELECT n.nome_produto,
            e.nome_emprestimos,
            e.id_disponibilidade,
            to_char(e.data_emprestimo, 'DD/MM/YYYY'::text) AS data_brasil,
            count(e.nu_patrimonio) AS quantidade_emprestada, s.descricao_disponibilidade
            FROM emprestimos e
            JOIN produtos_individuais pi ON pi.nu_patrimonio = e.nu_patrimonio
            JOIN nomes_produtos n ON n.id_produto = pi.id_produto
            JOIN status_disponibilidade_produto s ON s.id_disponibilidade = e.id_disponibilidade
            WHERE s.descricao_disponibilidade = 'Em atraso'::text OR s.descricao_disponibilidade = 'Emprestado'::text AND e.data_emprestimo >= (CURRENT_DATE - '30 days'::interval)
            GROUP BY n.nome_produto, e.nome_emprestimos, e.data_emprestimo, e.id_disponibilidade, s.descricao_disponibilidade
            ORDER BY e.data_emprestimo DESC;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_limpeza_e_higiene(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_limpeza_e_higiene
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Limpeza e Higiene'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_material_de_escritorio(conn):
        sql_select_view = """
           CREATE OR REPLACE VIEW visao_material_de_escritorio
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Material de Escritório'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_material_didatico(conn):
        sql_select_view = """
           CREATE OR REPLACE VIEW visao_material_didatico
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Material Didático'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_mobiliario(conn):
        sql_select_view = """
           CREATE OR REPLACE VIEW visao_mobiliario
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Mobiliário'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")

def criar_view_visao_outros(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_outros
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Outros'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
def criar_view_visao_salas_laboratorios(conn):
        sql_select_view = """
            CREATE OR REPLACE VIEW visao_salas_laboratorios
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Salas/Laboratórios'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")

def criar_view_visao_segurança(conn):
        sql_select_view = """
           CREATE OR REPLACE VIEW "visao_segurança"
            AS SELECT np.nome_produto AS "Produto",
            sp.descricao_status AS "Status Disponibilidade Atual",
            count(pi.nu_patrimonio) AS "Unidades (Total)"
            FROM produtos_individuais pi
            JOIN nomes_produtos np ON pi.id_produto = np.id_produto
            JOIN categorias_produto cp ON np.id_categoria = cp.id_categoria
            JOIN status_produto sp ON pi.id_status_produto = sp.id_status_produto
            WHERE cp.nome_categoria = 'Segurança'
            GROUP BY np.nome_produto, sp.descricao_status
            ORDER BY np.nome_produto, sp.descricao_status;
        """
        try:
            with conn.cursor() as cur:
                cur.execute(sql_select_view,)
            return True
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")

#   ================ CRIAÇÃO DAS VIEWS ===========================
        
def criar_todas_views(conn):

    # views Rita
    criar_view_produtos_exibicao_qtdAtivos(conn)
    criar_view_todos_produtos(conn)
    view_grafico_comparacao_ativos_inativos(conn)
    view_grafico_emprestimoCat_diarios(conn)
    view_grafico_itensPenCat(conn)
    criar_view_prod_disponiveis(conn)
    criar_view_produtos_emprestados_30_dias(conn)
    criar_view_devolucoes(conn)

    # views Ana
    criar_view_visao_audio_e_video(conn)
    criar_view_visao_eletrodomesticos(conn)
    criar_view_visao_equipamentos_eletronicos(conn)
    criar_view_visao_esportes_e_lazer(conn)
    criar_view_visao_historico_transacoes_emprestimos(conn)
    criar_view_visao_informatica(conn)
    criar_view_visao_infraestrutura(conn)
    criar_view_visao_itens_para_devolucao_30_dias(conn)
    criar_view_visao_limpeza_e_higiene(conn)
    criar_view_visao_material_de_escritorio(conn)
    criar_view_visao_material_didatico(conn)
    criar_view_visao_mobiliario(conn)
    criar_view_visao_outros(conn)
    criar_view_visao_salas_laboratorios(conn)
    criar_view_visao_segurança(conn)



