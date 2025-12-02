# database.py
"""
Responsável pela conexão com o banco de dados,
criação de tabelas e população de dados iniciais.
"""
import psycopg2
from src.config.config import DB_CONFIG

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

def pegar_linhas_da_view_do_banco(nome_view):
    """Essa função retorna a visao de determinada categoria"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {nome_view}")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def separar_o_retorno_por_variavel():
    """Pega a lista acima e guarda em variaveis o-pra usar depois"""
    pass

linhas = pegar_linhas_da_view_do_banco('visao_informatica')
print(type(linhas))

