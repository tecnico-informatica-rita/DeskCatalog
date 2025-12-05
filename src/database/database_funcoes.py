# database.py
"""
Responsável pela conexão com o banco de dados,
criação de tabelas e população de dados iniciais.
"""
import psycopg2
from psycopg2 import Error as ErroPsycopg2
from config.config import DB_CONFIG


#       EMPRÉSTIMOS

def buscar_id_por_disponibilidade(conn, nome_disponibilidade):
    sql_select = "SELECT id_disponibilidade FROM status_disponibilidade_produto WHERE descricao_disponibilidade = %s"

    with conn.cursor() as cur:
        cur.execute(sql_select, (nome_disponibilidade, ))
        resultados = cur.fetchone()

    return resultados[0] if resultados else None

def buscar_nuP_validos_por_id_produto(conn, nome, categoria):

    sql_select = """SELECT pi.nu_patrimonio FROM produtos_individuais AS pi
        JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
        JOIN categorias_produto AS c ON c.id_categoria = n.id_categoria
        JOIN status_produto AS s ON s.id_status_produto = pi.id_status_produto
        WHERE n.nome_produto = %s AND c.nome_categoria = %s
    """

    with conn.cursor() as cur:
        cur.execute(sql_select, (nome, categoria ))
        resultados = cur.fetchall()

    retorno = []
    for tupla in resultados:
        retorno.append(tupla[0])

    return retorno

def validar_nu_patrimonio_ativo(conn, nu_patrimonio):
    status = 'Ativo'

    sql_select = """SELECT 1 FROM produtos_individuais  AS pi 
        JOIN status_produto AS s ON pi.id_status_produto = s.id_status_produto
        WHERE pi.nu_patrimonio = %s AND s.descricao_status = %s"""

    with conn.cursor() as cur:
        cur.execute(sql_select, (nu_patrimonio, status))
        resultado = cur.fetchone()

    return resultado if resultado else None

def validar_nuP_disponivel(conn, nu_patrimonio):
    disponibilidade = 'Disponível'

    sql_select = """SELECT
        NOT EXISTS (
        SELECT 1
        FROM emprestimos AS e
        JOIN status_disponibilidade_produto AS s ON e.id_disponibilidade = s.id_disponibilidade
        WHERE e.nu_patrimonio = %s AND s.descricao_disponibilidade <> %s) AS pat_valido; """
    
    with conn.cursor() as cur:
        cur.execute(sql_select, (nu_patrimonio, disponibilidade))
        resultado = cur.fetchone()

    return resultado[0] if resultado else None


def validar_nu_patrimonio(conn, nome, categoria, qtd):
    if qtd <= 0 and not isinstance(qtd, int):
        raise ValueError ("Erro: quantidade inválida!")
    
    num_patrimonio = buscar_nuP_validos_por_id_produto(conn, nome, categoria)

    if not num_patrimonio:
        raise ValueError ("Erro: não foi encontrado nenhum número do patrimônio inválido para esse produto!")
    
    if len(num_patrimonio) < qtd:
        raise ValueError ("Erro: a quantidade esse produto não foi encotrada!")
    
    pat_validos = []

    for p in num_patrimonio:
        if len(pat_validos) == qtd:
            break

        esta_ativo = validar_nu_patrimonio_ativo(conn, p)
        if esta_ativo is not None:
            esta_disponivel = validar_nuP_disponivel(conn, p)
            if esta_disponivel is True:
                pat_validos.append(p)

    if len(pat_validos) < qtd:
        return False, pat_validos
    
    return True, pat_validos

def validar_emprestimo(conn, emprestimo, nu_patrimonio):
    id_disponibilidade = buscar_id_por_disponibilidade(conn, 'Emprestado')
    if not id_disponibilidade:
        raise ValueError ("Erro: disponibilidade inválida!")
    
    emprestimo.nu_patrimonio = nu_patrimonio
    emprestimo.id_disponibilidade = id_disponibilidade
    emprestimo.data_emprestimo = emprestimo.agora()
    emprestimo.data_devolucao = emprestimo.converter_data_timestamp()


def realizar_emprestimo(conn, emprestimo, qtd, pat_validos):
    sql_insert = """INSERT INTO emprestimos(nu_patrimonio, id_disponibilidade, data_devolucao, nome_emprestimos, data_emprestimo) 
                    VALUES (%s, %s, %s, %s, %s);"""

    if conn is None:
        raise ValueError("Erro com a conexão com o banco de dados.")
    
    emprestimo.validar()

    for p in pat_validos:
        validar_emprestimo(conn, emprestimo, p)

        try:
            with conn.cursor() as cur:
                cur.execute(sql_insert, (
                    emprestimo.nu_patrimonio, emprestimo.id_disponibilidade, emprestimo.data_devolucao,
                    emprestimo.nome_emprestimo, emprestimo.data_emprestimo
                    ))

        except (Exception, psycopg2.Error) as e:
            conn.rollback()
            raise ValueError(f"Erro ao realizar empréstimo: {e}")
        
    try:
        conn.commit()
        return True, len(pat_validos)
    except (Exception, psycopg2.Error) as e:
            conn.rollback()
            raise ValueError(f"Erro ao confirmar transação de empréstimo: {e}")
    
def buscar_produtos_emprestados(conn):
    sql_select_view = """
        SELECT 
n.nome_produto, c.nome_categoria, d.descricao_disponibilidade, e.nome_emprestimos, e.data_emprestimo, e.data_devolucao 
FROM emprestimos AS e
JOIN produtos_individuais AS pi ON pi.nu_patrimonio = e.nu_patrimonio
JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
JOIN categorias_produto AS c ON c.id_categoria = n.id_categoria
JOIN status_disponibilidade_produto AS d ON d.id_disponibilidade = e.id_disponibilidade
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql_select_view,)
        return True
    except Exception as e:
        raise ValueError (f"Erro inesperado ao realizar query: {e}")
    
def realizar_devolucao(conn):
    pass