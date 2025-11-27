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





def popular_dados_padrao(conn):
    """Popula o banco com dados iniciais se estiver vazio."""
    try:
        with conn.cursor() as cursor:
            # Verifica se já existem dados
            cursor.execute("SELECT COUNT(*) FROM salas")
            if cursor.fetchone()[0] > 0:
                print("ℹ️  Banco de dados já populado. Ignorando...")
                return

            # Inserir Salas
            salas = [
                (1, "Sala Digital"),
                (2, "Sala Premium")
            ]
            cursor.executemany("INSERT INTO salas (id, nome) VALUES (%s, %s)", salas)

            # Inserir Filmes
            filmes = [
                (1, "Aventura Espacial", "15:00", "matinê", 1, 15.00),
                (2, "Comédia Romântica", "16:30", "matinê", 2, 15.00),
                (3, "Thriller Noturno", "20:00", "noturno", 1, 20.00),
                (4, "Drama Épico", "21:30", "noturno", 2, 20.00)
            ]
            cursor.executemany("""
                INSERT INTO filmes (id, nome, horario, tipo, sala_id, preco) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, filmes)
            
            conn.commit()
            print("✅ Banco de dados populado com dados padrão.")
            
    except Exception as e:
        print(f"❌ Erro ao popular dados padrão: {e}")
        conn.rollback()


