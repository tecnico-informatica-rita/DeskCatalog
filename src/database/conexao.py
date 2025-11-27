import psycopg2
from src.database.database import get_db_connection, criar_tabelas

def criar_conexao(dbname="cinema_db", user="postgres", password="2007", host="localhost"):
    """
    Cria conexão com o banco PostgreSQL.
    
    Args:
        dbname (str): Nome do banco de dados
        user (str): Usuário
        password (str): Senha
        host (str): Host do banco
    
    Returns:
        connection: Objeto de conexão psycopg2
    """
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host
    )
    return conn

#teste_conexao_com_o_banco

conn = get_db_connection()
print("🔥 Conectado ao banco!")

criar_tabelas(conn)
print("🔥 Tabelas criadas com sucesso!")

conn.close()
print("✔️ Conexão fechada.")
