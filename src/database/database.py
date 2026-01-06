# database.py
"""
Responsável pela conexão com o banco de dados,
criação de tabelas e população de dados iniciais.
"""
import psycopg2
from config.config import DB_CONFIG

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Erro fatal ao conectar ao PostgreSQL: {e}")
        print("Verifique suas credenciais em 'config.py' e se o servidor está rodando.")
        raise e

def criar_tabelas(conn):
    """Cria as tabelas 'categorias_produto' e 'status_produto', 
    'status_disponibilidade_produto', 'etc' se não existirem."""

# -- tabelas de apoio:
    create_categorias_produto = """
    CREATE TABLE IF NOT EXISTS categorias_produto (
        id_categoria SERIAL PRIMARY KEY,
        nome_categoria TEXT NOT NULL
        
    );
    """

    create_status_produto = """
    CREATE TABLE IF NOT EXISTS status_produto (
        id_status_produto SERIAL PRIMARY KEY,
        descricao_status TEXT NOT NULL
    );
    """
    
    create_status_disponibilidade_produto = """
    CREATE TABLE IF NOT EXISTS status_disponibilidade_produto (
        id_disponibilidade SERIAL PRIMARY KEY,
        descricao_disponibilidade TEXT NOT NULL
    );
    """

    create_nomes_produtos = """
    CREATE TABLE IF NOT EXISTS nomes_produtos(
        id_produto SERIAL PRIMARY KEY,
        nome_produto TEXT NOT NULL UNIQUE,
        id_categoria INTEGER NOT NULL,

        FOREIGN KEY (id_categoria) REFERENCES categorias_produto(id_categoria)
        );
    """
# -- tabelas principais:
    create_produtos_individuais = """
    CREATE TABLE IF NOT EXISTS produtos_individuais (
        id_produto_individual SERIAL PRIMARY KEY,
        nu_patrimonio INTEGER GENERATED ALWAYS AS IDENTITY UNIQUE,
        id_produto INTEGER NOT NULL,
        id_status_produto INTEGER NOT NULL,
        FOREIGN KEY (id_produto) REFERENCES nomes_produtos(id_produto),
        FOREIGN KEY (id_status_produto) REFERENCES status_produto(id_status_produto)
    );
    """

    create_emprestimos = """
    CREATE TABLE IF NOT EXISTS emprestimos(
        id_emprestimo SERIAL PRIMARY KEY,
        nu_patrimonio SERIAL UNIQUE,
        id_disponibilidade INTEGER NOT NULL,
        data_devolucao TIMESTAMPTZ,
        nome_emprestimos TEXT NOT NULL,
        nome_devolucao TEXT NOT NULL,
        data_emprestimo TIMESTAMPTZ,
        devolvido_em TIMESTAMPTZ,
        FOREIGN KEY (id_disponibilidade) REFERENCES status_disponibilidade_produto(id_disponibilidade),
        FOREIGN KEY (nu_patrimonio) REFERENCES produtos_individuais(nu_patrimonio)
        );
    """

    
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_categorias_produto)
            cursor.execute(create_status_produto)
            cursor.execute(create_status_disponibilidade_produto)
            cursor.execute(create_nomes_produtos)
            cursor.execute(create_produtos_individuais)
            cursor.execute(create_emprestimos)

        conn.commit()
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        conn.rollback()


def popular_dados_login(lista_email_senha):
    """insere o login realizado no banco de dados"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            
            cursor.executemany(
                """
                INSERT INTO loguin_informacoes(email_login, senha_login)
                VALUES (%s, %s)
                ON CONFLICT (email_login) DO NOTHING;
                """,
                lista_email_senha
            )
            conn.commit()
            
            linhas = cursor.rowcount   #conta qts linhas inseriu

            if linhas == 0:
                return False, "⚠️ Email já existe no banco!"

            return True, "Inserido com sucesso!"

    except Exception as e:
        return False, f"❌ Erro ao salvar no banco: {str(e)}"
    

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



