# database.py
"""
Responsável pela conexão com o banco de dados,
criação de tabelas e população de dados iniciais.
"""
import psycopg2
from psycopg2 import Error as ErroPsycopg2
from src.config.config import DB_CONFIG

def buscar_nomes_produtos_existentes(conn):
    sql_select = """SELECT nome_produto FROM nomes_produtos"""

    with conn.cursor() as cur:
        cur.execute(sql_select)
        resultados = cur.fetchall()

    retorno = []
    for tupla in resultados:
        retorno.append(tupla[0])

    return retorno

def buscar_nome_categorias(conn):
    sql_select = """SELECT nome_categoria FROM categorias_produto"""

    with conn.cursor() as cur:
        cur.execute(sql_select)
        resultados = cur.fetchall()

    retorno = []
    for tupla in resultados:
        retorno.append(tupla[0])

    return retorno

def buscar_status(conn):
    sql_select = """SELECT descricao_status FROM status_produto"""

    with conn.cursor() as cur:
        cur.execute(sql_select)
        resultados = cur.fetchall()

    retorno = []
    for tupla in resultados:
        retorno.append(tupla[0])

    return retorno

def buscar_id_por_nome_produto(conn, nome):
    sql_select = "SELECT id_produto FROM nomes_produtos WHERE nome_produto = %s;"

    with conn.cursor() as cur:
        cur.execute(sql_select, (nome, ))
        resultados = cur.fetchone()

    return resultados[0] if resultados else None

def buscar_id_por_categoria(conn, categoria):
    sql_select = "SELECT id_categoria FROM categorias_produto WHERE nome_categoria = %s;"

    with conn.cursor() as cur:
        cur.execute(sql_select, (categoria, ))
        resultados = cur.fetchone()

    return resultados[0] if resultados else None
    
def buscar_id_por_status(conn, status):
    sql_select = "SELECT id_status_produto FROM status_produto WHERE descricao_status = %s;"

    with conn.cursor() as cur:
        cur.execute(sql_select, (status, ))
        resultados = cur.fetchone()

    return resultados[0] if resultados else None

def inserir_produto(conn, produto):
    sql_insert = "INSERT INTO produtos_individuais(id_produto, id_status_produto) VALUES (%s, %s)"

    try:
        with conn.cursor() as cur:
            cur.execute(sql_insert, (produto.id_produto, produto.id_status, ))
        return True
    except ErroPsycopg2:
        raise ValueError ("Erro ao adicionar produto!")
    except Exception:
        raise ValueError ("Erro inesperado ao adicionar produto!")
    
def inserir_varios_produtos_iguais(conn, produto):
    try:
        conn.autocommit = False

        for _ in range(produto.quantidade):
            inserir_produto(conn, produto)

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise ValueError("Erro ao adicionar produtos.\n")
    finally:
        conn.autocommit = True

def alterar_status(conn, novo_status: str):
    pass

def alterar_nome(conn, novo_nome: str):
    pass

def alterar_categoria(conn, nova_categoria: str):
    pass

