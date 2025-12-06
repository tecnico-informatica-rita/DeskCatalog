# database.py
"""
Responsável pela conexão com o banco de dados,
criação de tabelas e população de dados iniciais.
"""
import psycopg2
from psycopg2 import Error as ErroPsycopg2
from config.config import DB_CONFIG

def buscar_nomes_produtos_existentes(conn) -> list:
    sql_select = """SELECT nome_produto FROM nomes_produtos"""

    with conn.cursor() as cur:
        cur.execute(sql_select)
        resultados = cur.fetchall()

    retorno = []
    for tupla in resultados:
        retorno.append(tupla[0])

    return retorno

def buscar_nome_categorias(conn) -> list:
    sql_select = """SELECT nome_categoria FROM categorias_produto"""

    with conn.cursor() as cur:
        cur.execute(sql_select)
        resultados = cur.fetchall()

    retorno = []
    for tupla in resultados:
        retorno.append(tupla[0])

    return retorno

def buscar_status(conn) -> list:
    sql_select = """SELECT descricao_status FROM status_produto"""

    with conn.cursor() as cur:
        cur.execute(sql_select)
        resultados = cur.fetchall()

    retorno = []
    for tupla in resultados:
        retorno.append(tupla[0])

    return retorno

def buscar_id_por_nomeCategoria_produto(conn, nome, categoria) -> int:
    sql_select = "SELECT * FROM nomes_produtos WHERE nome_produto = %s AND id_categoria = %s;"

    id_categoria = buscar_id_por_categoria(conn, categoria)
    with conn.cursor() as cur:
        cur.execute(sql_select, (nome, id_categoria, ))
        resultados = cur.fetchone()

    return resultados[0] if resultados else None

def buscar_id_por_categoria(conn, categoria) -> int:
    sql_select = "SELECT id_categoria FROM categorias_produto WHERE nome_categoria = %s;"

    with conn.cursor() as cur:
        cur.execute(sql_select, (categoria, ))
        resultados = cur.fetchone()

    return resultados[0] if resultados else None
    
def buscar_id_por_status(conn, status) -> int:
    sql_select = "SELECT id_status_produto FROM status_produto WHERE descricao_status = %s;"

    with conn.cursor() as cur:
        cur.execute(sql_select, (status, ))
        resultados = cur.fetchone()

    return resultados[0] if resultados else None

def buscar_status_e_quantidade_por_produto(conn, produto):
    id_prod = buscar_id_por_nomeCategoria_produto(conn, produto.nome, produto.categoria)
    sql_select = "SELECT id_status_produto, COUNT(*) FROM produtos_individuais WHERE id_produto = %s GROUP BY id_status_produto;"

    with conn.cursor() as cur:
        cur.execute(sql_select, (id_prod, ))
        resultados = cur.fetchall()

    retorno = []
    for linha in resultados:
        dicio = {"id_status": linha[0], 
         "quantidade": linha[1]}
        retorno.append(dicio)
    return retorno if retorno else None

def inserir_produto(conn, produto) -> bool:
    sql_insert = "INSERT INTO produtos_individuais(id_produto, id_status_produto) VALUES (%s, %s)"

    try:
        with conn.cursor() as cur:
            cur.execute(sql_insert, (produto.id_produto, produto.id_status))
        return True
    except ErroPsycopg2:
        raise ValueError ("Erro ao adicionar produto!")
    except Exception:
        raise ValueError ("Erro inesperado ao adicionar produto!")
    
def inserir_varios_produtos_iguais(conn, produto) -> bool:
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

def adicionar_categoria(conn, categoria) -> bool:
    sql_insert = "INSERT INTO categorias_produto(nome_categoria) VALUES (%s)"

    try:
        with conn.cursor() as cur:
            cur.execute(sql_insert, (categoria, ))
        return True
    except ErroPsycopg2:
        raise ValueError ("Erro ao adicionar categoria!")
    except Exception:
        raise ValueError ("Erro inesperado ao adicionar categoria!")
    
def adicionar_status(conn, status) -> bool:
    sql_insert = "INSERT INTO status_produto(descricao_status) VALUES (%s)"

    try:
        conn.autocommit = False
        with conn.cursor() as cur:
            cur.execute(sql_insert, (status, ))
        conn.commit()
        return True
    except ErroPsycopg2:
        conn.rollback()
        raise ValueError ("Erro ao adicionar status!")
    except Exception:
        raise ValueError ("Erro inesperado ao adicionar status!")
    finally:
        conn.autocommit = True

def adicionar_nome(conn, nome, id_categoria) -> bool:
    sql_insert = "INSERT INTO nomes_produtos(nome_produto, id_categoria) VALUES (%s, %s)"

    try:
        conn.autocommit = False
        with conn.cursor() as cur:
            cur.execute(sql_insert, (nome, id_categoria ))
        conn.commit()
        return True
    except ErroPsycopg2:
        conn.rollback()
        raise ValueError ("Erro ao adicionar nome!")
    except Exception:
        raise ValueError ("Erro inesperado ao adicionar nome!")
    finally:
        conn.autocommit = True
def alterar_status(conn, produto, status_antigo:str):
    id_status_novo = buscar_id_por_status(conn, produto.novo_status)
    id_prod = buscar_id_por_nomeCategoria_produto(conn, produto.nome, produto.categoria)
    id_status_antigo = buscar_id_por_status(conn, status_antigo)

    if not id_status_novo:
        raise ValueError (f"Erro: O Status '{produto.status}' não foi encontrado no catálogo.")
    if not id_status_antigo:
        raise ValueError (f"Erro: O Status '{status_antigo}' não foi encontrado no catálogo.")
    if not id_prod:
        raise ValueError ("Esse produto não existe no catálogo.\n")
    if id_status_antigo == id_status_novo:
        raise ValueError ("Operação redundante, o status é o mesmo.")
    
    sql_buscar = "SELECT nu_patrimonio FROM produtos_individuais WHERE id_status_produto = %s AND id_produto = %s ORDER BY nu_patrimonio ASC LIMIT %s;"
    sql_update = "UPDATE produtos_individuais SET id_status_produto = %s WHERE nu_patrimonio = %s"

    try:
        conn.autocommit = False
        with conn.cursor() as cur:
            cur.execute(sql_buscar, (id_status_antigo, id_prod, produto.quantidade))
            lista_patrimonios = cur.fetchall()

            if len(lista_patrimonios) < produto.quantidade:
                raise ValueError(f"Existem apenas {len(lista_patrimonios)} unidades com status '{status_antigo}'.")
            
            for (patrimonio,) in lista_patrimonios:
                cur.execute(sql_update, (id_status_novo, patrimonio))
                lista_patrinomios = cur.fetchall()
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise ValueError ("Erro inesperado ao alterar status!")
    finally:
        conn.autocommit = True

def alterar_nome(conn, novo_nome: str, produto):
    pass

def alterar_categoria(conn, nova_categoria: str, produto):
    pass

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
    
def exibir_todos_produtos_qtdAtivos(conn):
    with conn.cursor() as cur:
        sql_select = "SELECT * FROM vw_todos_produtos_qtdAtivos"
        cur.execute(sql_select)
        rows = cur.fetchall()
        return rows
    
def exibir_todos_produtos(conn):
    with conn.cursor() as cur:
        sql_select = "SELECT * FROM vw_todos_produtos"
        cur.execute(sql_select)
        rows = cur.fetchall()
        return rows
    


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
    disponibilidade = 'Emprestado'

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
    
    
    #       DEVOLUÇÕES
    
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
    
def criar_view_historico_emprestados(conn):
    sql_select_view = """
        CREATE OR REPLACE VIEW vw_historico_transacoes_emprestimos AS
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
        return True
    except Exception as e:
        raise ValueError (f"Erro inesperado ao realizar query: {e}")
    
def exibir_itens_para_devolucao_30(conn):
    with conn.cursor() as cur:
        sql_select = "SELECT * FROM vw_itens_para_devolucao_30"
        cur.execute(sql_select)
        rows = cur.fetchall()
    return rows
    
def exibir_historico_transacoes_emprestimos(conn):
    with conn.cursor() as cur:
        sql_select = "SELECT * FROM vw_historico_transacoes_emprestimos"
        cur.execute(sql_select)
        rows = cur.fetchall()
    return rows

def buscar_nuP_emprestimo(conn, nome_produto, emprestimo, qtd):
    sql_select_view = """
        SELECT e.nu_patrimonio
        FROM emprestimos AS e
        JOIN produtos_individuais AS pi ON pi.nu_patrimonio = e.nu_patrimonio
        JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
        JOIN status_disponibilidade_produto AS s ON s.id_disponibilidade = e.id_disponibilidade
        WHERE s.descricao_disponibilidade IN ('Emprestado', 'Em atraso') 
            AND n.nome_produto = %s
            AND e.nome_emprestimos = %s
            AND e.data_emprestimo::date = %s
        LIMIT %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql_select_view, (nome_produto, emprestimo.nome_emprestimo, emprestimo.data_emprestimo, qtd))
            resultados = cur.fetchall()
        retorno = []
        for tupla in resultados:
            retorno.append(tupla[0])

        return retorno
    except Exception as e:
        raise ValueError (f"Erro inesperado ao realizar query: {e}")
    
def validar_nuP_emprestimo(conn, nu_patrimonio):
    sql_select = """SELECT 1 FROM produtos_individuais  AS pi 
        JOIN emprestimos AS e ON pi.nu_patrimonio = e.nu_patrimonio
        WHERE pi.nu_patrimonio = %s AND e.devolvido_em IS NULL AND e.nome_devolucao IS NULL"""

    with conn.cursor() as cur:
        cur.execute(sql_select, (nu_patrimonio,))
        resultado = cur.fetchone()

    return resultado if resultado else None
    
def validar_nuP_devolucao(conn, nome_produto, emprestimo, qtd):
    try:
        qtd = int(qtd)
        if qtd <= 0:
            raise ValueError ("Erro: quantidade inválida!")
    except Exception as e:
        raise ValueError ("Erro: quantidade inválida, digite apenas números!")
    
    num_patrimonio = buscar_nuP_emprestimo(conn, nome_produto, emprestimo, qtd)

    if not num_patrimonio:
        raise ValueError ("Erro: não foi encontrado nenhum número do patrimônio válido para essa devolução!")
    
    if len(num_patrimonio) < qtd:
        raise ValueError ("Erro: a quantidade esse produto não foi encotrada!")
    
    pat_validos = []

    for p in num_patrimonio:
        if len(pat_validos) == qtd:
            break
    
        precisa_devolver = validar_nu_patrimonio_ativo(conn, p)
        if precisa_devolver is not None:
                pat_validos.append(p)

    if len(pat_validos) < qtd:
        return False, pat_validos
    
    return True, pat_validos

def validar_devolucao(conn, emprestimo, nu_patrimonio):
    id_disponibilidade_devolvido = buscar_id_por_disponibilidade(conn, 'Devolvido')
    id_disponibilidade_devolvido = buscar_id_por_disponibilidade(conn, 'Devolvido')
    if not id_disponibilidade:
        raise ValueError ("Erro: disponibilidade inválida!")
    
    emprestimo.nu_patrimonio = nu_patrimonio
    emprestimo.id_disponibilidade = id_disponibilidade
    emprestimo.data_emprestimo = emprestimo.agora()
    emprestimo.data_devolucao = emprestimo.converter_data_timestamp()

def realizar_devolucao(conn):
    pass