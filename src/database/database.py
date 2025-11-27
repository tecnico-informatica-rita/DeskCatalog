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
    """Cria as tabelas 'salas' e 'filmes' se não existirem."""
    create_salas_query = """
    CREATE TABLE IF NOT EXISTS salas (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL
    );
    """
    
    create_filmes_query = """
    CREATE TABLE IF NOT EXISTS filmes (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        horario VARCHAR(5) NOT NULL,
        tipo VARCHAR(10) NOT NULL,
        sala_id INT NOT NULL REFERENCES salas(id),
        preco NUMERIC(10, 2) NOT NULL
    );
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_salas_query)
            cursor.execute(create_filmes_query)
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


