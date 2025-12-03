import psycopg2
from psycopg2 import Error as ErroPsycopg2

def inserir_categorias_produto(conn):
    categorias = [
    ('Mobiliário',),
    ('Informática',),
    ('Material Didático',),
    ('Material de Escritório',),
    ('Eletrodomésticos',),
    ('Equipamentos Eletrônicos',),
    ('Limpeza e Higiene',),
    ('Infraestrutura',),
    ('Segurança',),
    ('Salas/Laboratórios',),
    ('Áudio e Vídeo',),
    ('Esportes e Lazer',),
    ('Outros',)
    ]

    sql_insert = "INSERT INTO categorias_produto (nome_categoria) VALUES (%s)"

    if conn is None:
        raise ValueError("Erro com a conexão com o banco de dados.")

    try:
        with conn.cursor() as cur:
            cur.executemany(sql_insert, categorias, )
            inseridos = cur.rowcount
        conn.commit()
        return inseridos
    
    except (Exception, psycopg2.Error) as e:
        conn.rollback()
        raise ValueError (f" Erro ao inserir dados no PostgreSQL: {e}")
        

def inserir_status_produto(conn):
    status = [
        ('Ativo',),
        ('Inativo',),
        ('Em Manutenção',),
        ('Perdido',),
    ]

    sql_insert = "INSERT INTO status_produto (descricao_status) VALUES (%s)"

    if conn is None:
        raise ValueError("Erro com a conexão com o banco de dados.")

    try:
        with conn.cursor() as cur:
            cur.executemany(sql_insert, status)
            inseridos = cur.rowcount
        conn.commit()
        return inseridos

    except (Exception, psycopg2.Error) as e:
        conn.rollback()
        raise ValueError (f"Erro ao inserir dados no PostgreSQL: {e}")
        
def inserir_status_disponibilidade_produto(conn):
    disponibilidade = [
        ('Emprestado',),
        ('Devolvido',),
        ('Em atraso',),
    ]

    sql_insert = "INSERT INTO status_disponibilidade_produto (descricao_disponibilidade) VALUES (%s)"

    if conn is None:
        raise ValueError("Erro com a conexão com o banco de dados.")

    try:
        with conn.cursor() as cur:
            cur.executemany(sql_insert, disponibilidade)
            
            inseridos = cur.rowcount
        conn.commit()
        return inseridos

    except (Exception, psycopg2.Error) as e:
        conn.rollback()
        raise ValueError (f"Erro ao inserir dados no PostgreSQL: {e}")
        