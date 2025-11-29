# database.py
"""
Responsável pela conexão com o banco de dados,
criação de tabelas e população de dados iniciais.
"""
import psycopg2
from src.config.config import DB_CONFIG

def buscar_nomes_produtos_existentes(conn):
    sql_select = """SELECT nome_produto FROM nomes_produtos"""

    with conn.cursor() as cur:
        cur.execute(sql_select)
        resultados = cur.fetchall()

    return resultados

def buscar_nome_categorias(conn):
    sql_select = """SELECT nome_categoria FROM categorias_produto"""

    with conn.cursor() as cur:
        cur.execute(sql_select)
        resultados = cur.fetchall()

    return resultados

def buscar_status(conn):
    sql_select = """SELECT descricao_status FROM status_produto"""

    with conn.cursor() as cur:
        cur.execute(sql_select)
        resultados = cur.fetchall()

    return resultados

def buscar_id_por_nome_produto(conn, nome):
    pass

def inserir_varios_produtos_iguais(conn, qtd: str):
    pass

def alterar_status(conn, novo_status: str):
    pass

def alterar_nome(conn, novo_nome: str):
    pass

def alterar_categoria(conn, nova_categoria: str):
    pass