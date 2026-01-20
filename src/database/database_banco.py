import psycopg2
import csv
from config.config import DB_CONFIG
from database.viewsBanco import criar_todas_views
"""
Responsável pela conexão com o banco de dados,
criação de tabelas e população de dados iniciais.
"""

ARQUIVO_CSV = 'produtosCerto.csv'

#   ================ CONEXÃO COM O BANCO ==============

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Erro fatal ao conectar ao PostgreSQL: {e}")
        print("Verifique suas credenciais em 'config.py' e se o servidor está rodando.")
        raise e

#   ================ CRIAÇÃO DAS TABELAS ==============

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
        nome_devolucao TEXT NULL,
        data_emprestimo TIMESTAMPTZ,
        devolvido_em TIMESTAMPTZ,
        
        FOREIGN KEY (id_disponibilidade) REFERENCES status_disponibilidade_produto(id_disponibilidade),
        FOREIGN KEY (nu_patrimonio) REFERENCES produtos_individuais(nu_patrimonio)
        );
    """

    create_loguin_informacoes = """
    CREATE TABLE IF NOT EXISTS loguin_informacoes(
        id_loguin SERIAL PRIMARY KEY,
        email_login TEXT NOT NULL UNIQUE,
        senha_login TEXT NOT NULL
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
            cursor.execute(create_loguin_informacoes)

        conn.commit()
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        conn.rollback()


#   ================ INSERÇÕES NO BANCO ==============

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
        return inseridos
    
    except (Exception, psycopg2.Error) as e:
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
        return inseridos

    except (Exception, psycopg2.Error) as e:
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
        return inseridos

    except (Exception, psycopg2.Error) as e:
        raise ValueError (f"Erro ao inserir dados no PostgreSQL: {e}")
    
# Inserir os produtos através de um arquivo CSV ----------------------------------------------------------------------------
id_categoria = {}
id_status = {}

def get_id_categoria(conn, categoria):
    global id_categoria

    if categoria in id_categoria:
        return id_categoria[categoria]
    
    sql_select = "SELECT id_categoria FROM categorias_produto WHERE nome_categoria = %s;"

    with conn.cursor() as cur:
        cur.execute(sql_select, (categoria, ))
        resultados = cur.fetchone()

    if resultados:
        id_categoria[categoria] = resultados[0]
        return resultados[0]
    return None

def get_id_status(conn, status):
    global id_status

    if status in id_status:
        return id_status[status]
    
    sql_select = "SELECT id_status_produto FROM status_produto WHERE descricao_status = %s;"

    with conn.cursor() as cur:
        cur.execute(sql_select, (status, ))
        resultados = cur.fetchone()

    if resultados:
        id_status[status] = resultados[0]
        return resultados[0]
    return None

def inserir_nomes_produtos_e_individuais(conn):

    if conn is None:
        raise ValueError("Erro com a conexão com o banco de dados.")

    try:
        with conn.cursor() as cur:
            with open(ARQUIVO_CSV, mode='r', encoding='utf-8') as arq:
                dados = csv.reader(arq, delimiter=';')
                next(dados) 
                
                sql_insert_produto = "INSERT INTO nomes_produtos (id_categoria, nome_produto) VALUES (%s, %s) RETURNING id_produto;"
                sql_insert_produtos_individuais = "INSERT INTO produtos_individuais (id_produto, id_status_produto) VALUES (%s, %s);"
                
                for linha in dados:
                    nome_categoria_csv = linha[0].strip()
                    nome_produto = linha[1].strip()
                    status_csv = linha[3].strip()
                    
                    try:
                        quantidade = int(linha[2].strip())
                    except (IndexError, ValueError) as e:
                        raise ValueError("Erro de quantidade.")
                    
                    id_categoria = get_id_categoria(conn, nome_categoria_csv)
                    
                    if id_categoria is not None:
                        cur.execute(sql_insert_produto, (id_categoria, nome_produto))

                        produto_id_resultado = cur.fetchone()
                        
                        if produto_id_resultado:
                            id_produto_inserido = produto_id_resultado[0]
                            id_status = get_id_status(conn, status_csv)

                            if id_status is not None:
                                for _ in range(quantidade):
                                    cur.execute(sql_insert_produtos_individuais, (id_produto_inserido, id_status))
                    
    except (Exception, psycopg2.Error) as e:
        raise ValueError (f"Erro ao inserir dados no PostgreSQL: {e}")
    

#   ================ POPULA O BANCO E CRIA AS VIEW ==============

def popular_dados_padrao(conn):
    """Popula o banco com dados iniciais se estiver vazio."""
    try:
        with conn.cursor() as cursor:
            # Verifica se já existem dados
            cursor.execute("SELECT COUNT(*) FROM nomes_produtos")
            if cursor.fetchone()[0] == 0:
                # Populando
                inserir_categorias_produto(conn)
                inserir_status_produto(conn)
                inserir_status_disponibilidade_produto(conn)
                inserir_nomes_produtos_e_individuais(conn)
                conn.commit()
                print("✅ Dados padrão inseridos.")
            else:
                print("ℹ️  Banco de dados já populado. Ignorando...")
                
            # Depois crie as views
            criar_todas_views(conn)
            conn.commit() # Commit para salvar a criação da view (se necessário)
            print("✅ Views criadas ou atualizadas com sucesso.")
        
    except Exception as e:
        print(f"❌ Erro ao popular dados padrão: {e}")
        conn.rollback()


#   ================ INSERE LOGIN NO BANCO ==============

def popular_dados_login(conn, lista_email_senha):
    """insere o login realizado no banco de dados"""
    try:
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
        conn.rollback()
        return False, f"❌ Erro ao salvar no banco: {str(e)}"
    