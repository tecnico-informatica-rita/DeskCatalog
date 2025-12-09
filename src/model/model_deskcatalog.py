# model.py
"""
Camada Model (Modelo):
- Define as classes de entidade (Produto, Empréstimo).
- Define as classes de acesso a dados (GerenciadorProduto).
- Define a lógica de negócios e cálculos (GerenciadorLanchonete, Calculos).
"""

from datetime import datetime as dt
from psycopg2 import Error as ErroPsycopg2
import pytz

# ====== MENSAGENS PADRONIZADAS ======
MSG = {
    "sucesso_add_qtd": {"status": "ok", "mensagem": "Quantidade adicionada ao estoque!"},
    "sucesso_add_prod": {"status": "ok", "mensagem": "Produto adicionado ao catálogo! 🎉"},
    "erro_ja_cadastrado": {"status": "erro", "mensagem": "Esse produto já existe no catálogo!"},
    "erro_ja_cadastrado_outraC": {"status": "erro", "mensagem": "Esse produto já está cadastrado com outra categoria."},
    "erro_nome_invalido": {"status": "erro", "mensagem": "Nome inválido!"},
    "erro_categoria_invalida": {"status": "erro", "mensagem": "Categoria inválida!"},
    "erro_status_invalido": {"status": "erro", "mensagem": "Status inválido!"},
    "erro_qtd_invalida": {"status": "erro", "mensagem": "Quantidade inválida!"},
    "erro_qtd_invalida_tipo": {"status": "erro", "mensagem": "Quantidade inválida, digite apenas números inteiros!"},
    "erro_geral": {"status": "erro", "mensagem": "Erro inesperado, contate o suporte!"},
    "erro_inserir_prod": {"status": "erro","mensagem": "Erro ao adicionar produto!"},
    "erro_inserir_inesperado": {"status": "erro","mensagem": "Erro inesperado ao adicionar produto!"},
    "sucesso_inserir": {"status": "ok","mensagem": "Produto adicionado com sucesso!"},
    "sucesso_inserir_varios": {"status": "ok","mensagem": "Produtos adicionados com sucesso!"},
    "erro_adicionar_nome" : {"status": "erro","mensagem": "Erro inesperado ao adicionar nome!"},
    "erro_id_interno": {"status": "erro","mensagem": "Erro interno: Falha ao confirmar o ID do produto recém-cadastrado."}
}

# ==================== CLASSES DE ENTIDADE ====================

#PODEMOS USAR ESSA CLASSE PARA SER NOSSO CATALOGO

class Produto:
    """Classe que representa um produto no sistema do catálogo"""

    """Recebe da view em string e depois para inserir no banco converte para o id"""
    def __init__(self, nome: str, categoria: str, quantidade: str, status: str):
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.status = status
        self.nu_patrimonio = None
        self.id_produto = None
        self.id_status = None

    def validar(self):
        if not self.nome and not self.categoria and not self.status and not self.quantidade:
                raise ValueError("Preencha todos os campos obrigatórios!")
        
        try:
            self.quantidade = int(self.quantidade)
            if self.quantidade <= 0:
                raise ValueError(MSG["erro_qtd_invalida"]["mensagem"])
        except ValueError:
            raise ValueError(MSG["erro_qtd_invalida_tipo"]["mensagem"])
        if not self.nome or not self.nome.strip():
            raise ValueError (MSG["erro_nome_invalido"]["mensagem"])
        else:
            self.nome = self.nome.capitalize()
        if not self.categoria or not self.categoria.strip():
            raise ValueError (MSG["erro_categoria_invalida"]["mensagem"])
        if not self.status or not self.status.strip():
            raise ValueError (MSG["erro_status_invalido"]["mensagem"])
        
    def produto_banco(self, id_produto, id_status):
        self.id_produto = id_produto
        self.id_status = id_status


class Emprestimo:
    """Classe que representa um emprestimo no sistema do catálogo"""

    tz = pytz.timezone('America/Sao_Paulo')

    def __init__(self, nome_emprestimo: str, data_devolucao: str, nu_patrimonio = -1, nome_devolucao = "Sem devolução"):
        self.nu_patrimonio = nu_patrimonio
        self.id_disponibilidade = None
        self.nome_devolucao = nome_devolucao.strip().title()
        self.nome_emprestimo = nome_emprestimo.strip().title()
        self.data_devolucao = data_devolucao
        self.devolveu_em = None
        self.data_emprestimo = None
        

    def validar(self):
        if not self.nome_emprestimo and not self.data_devolucao:
                raise ValueError("Preencha todos os campos obrigatórios!")
        
        if not self.nome_devolucao:
            raise ValueError ("Nome do devolutor inválido.")
        if not self.nome_emprestimo:
            raise ValueError ("Nome do solicitador inválido.")
        if not self.data_devolucao:
            raise ValueError ("Preencha a data de devolução!")
        
        if not self.nu_patrimonio or not isinstance(self.nu_patrimonio, int):
            raise ValueError ("Número do patrimônio inválido.")
        
        data_datetime = self.data_devolucao_str_para_date()
        hoje = dt.now(self.tz).date()

        if data_datetime < hoje:
            raise ValueError ("A data não pode estar no passado.")
        
    # O DatePicker retorna string “YYYY-MM-DD”
    def data_devolucao_str_para_date(self) -> dt.date:
        data_formatada = str(self.data_devolucao).replace("T", " ").split(" ")[0]
        return dt.strptime(data_formatada, "%Y-%m-%d").date()
        
        
    def converter_data_timestamp(self):
        data_datetime = self.data_devolucao_str_para_date()

        data = dt(
            year=data_datetime.year,
            month=data_datetime.month,
            day=data_datetime.day,
            hour=0,
            minute=0,
            second=0
        )
        
        return self.tz.localize(data)
    
    def converter_data_string(self):
        pass
        
    def agora(self):
        return dt.now(self.tz)
    

class Alteracoes:
    pass



    # ==================== CLASSES DE ACESSO A DADOS (REPOSITÓRIO) ===========

class GerenciadorProduto:
    """Classe responsável por buscar dados sobre o produto no banco de dados."""
    
    def __init__(self, conn):
        """Recebe uma conexão com o banco de dados."""
        self.conn = conn

    def buscar_nomes_produtos_existentes(self) -> list:
        sql_select = """SELECT nome_produto FROM nomes_produtos"""

        with self.conn.cursor() as cur:
            cur.execute(sql_select)
            resultados = cur.fetchall()

        retorno = []
        for tupla in resultados:
            retorno.append(tupla[0])

        return retorno

    def buscar_nome_categorias(self) -> list:
        sql_select = """SELECT nome_categoria FROM categorias_produto"""

        with self.conn.cursor() as cur:
            cur.execute(sql_select)
            resultados = cur.fetchall()

        retorno = []
        for tupla in resultados:
            retorno.append(tupla[0])

        return retorno

    def buscar_status(self) -> list:
        sql_select = """SELECT descricao_status FROM status_produto"""

        with self.conn.cursor() as cur:
            cur.execute(sql_select)
            resultados = cur.fetchall()

        retorno = []
        for tupla in resultados:
            retorno.append(tupla[0])

        return retorno

    def buscar_id_por_nomeCategoria_produto(self, nome, categoria) -> int:
        sql_select = "SELECT * FROM nomes_produtos WHERE LOWER(nome_produto) = LOWER(%s) AND id_categoria = %s;"

        id_categoria = self.buscar_id_por_categoria(categoria)
        with self.conn.cursor() as cur:
            cur.execute(sql_select, (nome, id_categoria, ))
            resultados = cur.fetchone()

        return resultados[0] if resultados else None
    
    def buscar_dados_produto_por_nome(self, nome: str):
        sql_select = """
            SELECT id_produto, id_categoria 
            FROM nomes_produtos 
            WHERE LOWER(nome_produto) = LOWER(%s);
        """
        with self.conn.cursor() as cur:
            cur.execute(sql_select, (nome, ))
            resultado = cur.fetchone()
            
        if resultado:
            return {"id_produto": resultado[0], "id_categoria": resultado[1]}
        return None

    def buscar_id_por_categoria(self, categoria) -> int:
        sql_select = "SELECT id_categoria FROM categorias_produto WHERE LOWER(nome_categoria) = LOWER(%s);"

        with self.conn.cursor() as cur:
            cur.execute(sql_select, (categoria, ))
            resultados = cur.fetchone()

        return resultados[0] if resultados else None
    
    def buscar_id_por_status(self, status) -> int:
        sql_select = "SELECT id_status_produto FROM status_produto WHERE descricao_status = %s;"

        with self.conn.cursor() as cur:
            cur.execute(sql_select, (status, ))
            resultados = cur.fetchone()

        return resultados[0] if resultados else None

    def buscar_status_e_quantidade_por_produto(self, produto):
        id_prod = self.buscar_id_por_nomeCategoria_produto(produto.nome, produto.categoria)
        sql_select = "SELECT id_status_produto, COUNT(*) FROM produtos_individuais WHERE id_produto = %s GROUP BY id_status_produto;"

        with self.conn.cursor() as cur:
            cur.execute(sql_select, (id_prod, ))
            resultados = cur.fetchall()

        retorno = []
        for linha in resultados:
            dicio = {"id_status": linha[0], 
                    "quantidade": linha[1]}
            retorno.append(dicio)
        return retorno if retorno else None

    def inserir_produto(self, produto) -> bool:
        sql_insert = "INSERT INTO produtos_individuais(id_produto, id_status_produto) VALUES (%s, %s)"

        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_insert, (produto.id_produto, produto.id_status))
                return True
        except ErroPsycopg2:
            raise ValueError (MSG["erro_inserir_prod"]["mensagem"])
        except Exception as e:
            raise ValueError (MSG["erro_inserir_inesperado"]["mensagem"])
    
    def inserir_varios_produtos_iguais(self, produto) -> bool:
        try:
            with self.conn:  # inicia e controla a transação automaticamente
                for _ in range(produto.quantidade):
                    self.inserir_produto(produto)
            return True

        except Exception as e:
            raise ValueError(MSG["erro_inserir_prod"]["mensagem"])

    def exibir_todos_produtos_qtdAtivos(self):
        with self.conn.cursor() as cur:
            sql_select = "SELECT * FROM vw_todos_produtos_qtdAtivos"
            cur.execute(sql_select)
            rows = cur.fetchall()
            return rows
    
    def exibir_todos_produtos(self):
        with self.conn.cursor() as cur:
            sql_select = "SELECT * FROM vw_todos_produtos"
            cur.execute(sql_select)
            rows = cur.fetchall()
            return rows

class GerenciarEmprestimo:
    """Classe responsável por buscar dados sobre o empréstimo no banco de dados."""
    
    def __init__(self, conn):
        """Recebe uma conexão com o banco de dados."""
        self.conn = conn

    def buscar_id_por_disponibilidade(self, nome_disponibilidade):
        sql_select = "SELECT id_disponibilidade FROM status_disponibilidade_produto WHERE descricao_disponibilidade = %s"

        with self.conn.cursor() as cur:
            cur.execute(sql_select, (nome_disponibilidade, ))
            resultados = cur.fetchone()

        return resultados[0] if resultados else None

    def buscar_nuP_validos_por_id_produto(self, nome, categoria):

        sql_select = """SELECT pi.nu_patrimonio FROM produtos_individuais AS pi
            JOIN nomes_produtos AS n ON n.id_produto = pi.id_produto
            JOIN categorias_produto AS c ON c.id_categoria = n.id_categoria
            JOIN status_produto AS s ON s.id_status_produto = pi.id_status_produto
            WHERE LOWER(n.nome_produto) = LOWER(%s) AND LOWER(c.nome_categoria) = LOWER(%s)
        """

        with self.conn.cursor() as cur:
            cur.execute(sql_select, (nome, categoria ))
            resultados = cur.fetchall()

        retorno = []
        for tupla in resultados:
            retorno.append(tupla[0])

        return retorno

    def validar_nu_patrimonio_ativo(self, nu_patrimonio):
        status = 'Ativo'

        sql_select = """SELECT 1 FROM produtos_individuais  AS pi 
            JOIN status_produto AS s ON pi.id_status_produto = s.id_status_produto
            WHERE pi.nu_patrimonio = %s AND s.descricao_status = %s"""

        with self.conn.cursor() as cur:
            cur.execute(sql_select, (nu_patrimonio, status))
            resultado = cur.fetchone()

        return resultado if resultado else None

    
    def validar_nuP_disponivel(self, nu_patrimonio):
        sql_select = """
            SELECT CASE 
                 WHEN s.descricao_disponibilidade = 'Emprestado' THEN FALSE
                 ELSE TRUE
               END AS pat_valido
            FROM emprestimos AS e
            JOIN status_disponibilidade_produto AS s 
             ON e.id_disponibilidade = s.id_disponibilidade
            WHERE e.nu_patrimonio = %s
            ORDER BY e.data_emprestimo DESC
            LIMIT 1;
    """

        with self.conn.cursor() as cur:
            cur.execute(sql_select, (nu_patrimonio,))
            resultado = cur.fetchone()

    # Se nunca existiu empréstimo, está disponível
        if resultado is None:
            return True

        return resultado[0]



    def validar_nu_patrimonio(self, nome, categoria, qtd):
        try:
            qtd = int(qtd)
            if qtd <= 0:
                raise ValueError(MSG["erro_qtd_invalida"]["mensagem"])
        except ValueError:
            raise ValueError(MSG["erro_qtd_invalida_tipo"]["mensagem"])
        
        if not nome or not categoria:
            raise ValueError ("Preencha o nome e categoria do item!")
        
        num_patrimonio = self.buscar_nuP_validos_por_id_produto( nome, categoria)

        if num_patrimonio is None:
            raise ValueError ("Erro: não foi encontrado nenhum número do patrimônio válido para esse produto!")

        if len(num_patrimonio) == 0:
            raise ValueError ("Não há nenhum item disponível para empréstimo!")
        
        if len(num_patrimonio) < qtd:
            #raise ValueError ("Erro: a quantidade esse produto não foi encotrada!")
            return False, num_patrimonio
    
        pat_validos = []

        for p in num_patrimonio:
            if len(pat_validos) == qtd:
                break

            esta_ativo = self.validar_nu_patrimonio_ativo( p)
            if esta_ativo:
                esta_disponivel = self.validar_nuP_disponivel( p)
                if esta_disponivel is True:
                    pat_validos.append(p)

        if len(pat_validos) < qtd:
            return False, pat_validos
    
        return True, pat_validos

    def validar_emprestimo(self, emprestimo, nu_patrimonio):
        id_disponibilidade = self.buscar_id_por_disponibilidade( 'Emprestado')
        if not id_disponibilidade:
            raise ValueError ("Erro: disponibilidade inválida!")
    
        emprestimo.nu_patrimonio = nu_patrimonio
        emprestimo.id_disponibilidade = id_disponibilidade
        emprestimo.data_emprestimo = emprestimo.agora()
        emprestimo.data_devolucao = emprestimo.converter_data_timestamp()


    def realizar_emprestimo(self, emprestimo, qtd, pat_validos):
        sql_insert = """INSERT INTO emprestimos(nu_patrimonio, id_disponibilidade, data_devolucao, nome_emprestimos, data_emprestimo) 
                        VALUES (%s, %s, %s, %s, %s);"""
        
        '''sql_insert = """
        INSERT INTO emprestimos(nu_patrimonio, id_disponibilidade, data_devolucao, nome_emprestimos, data_emprestimo)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (nu_patrimonio) DO UPDATE SET
        id_disponibilidade = EXCLUDED.id_disponibilidade,
        data_devolucao     = EXCLUDED.data_devolucao,
        nome_emprestimos   = EXCLUDED.nome_emprestimos,
        data_emprestimo    = EXCLUDED.data_emprestimo;
        """'''

        if self.conn is None:
            raise ValueError("Erro com a conexão com o banco de dados.")
    
        emprestimo.validar()

        try:
            registrados = 0

            with self.conn.cursor() as cur:
                for p in pat_validos:
                    if not self.validar_nuP_disponivel(p):
                        continue

                    emp = Emprestimo(nome_emprestimo = emprestimo.nome_emprestimo, data_devolucao = emprestimo.data_devolucao, nu_patrimonio = p)
                    self.validar_emprestimo(emp, p)
        
                    cur.execute(sql_insert, (
                        emp.nu_patrimonio, emp.id_disponibilidade, emp.data_devolucao,
                        emp.nome_emprestimo, emp.data_emprestimo))
                    registrados += 1

                self.conn.commit()
                return True, registrados
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Erro ao realizar empréstimo: {e}")
        
    def exibir_produtos_disponiveis(self):
        with self.conn.cursor() as cur:
            sql_select = "SELECT * FROM vw_produtos_disponiveis"
            cur.execute(sql_select)
            rows = cur.fetchall()
            return rows
    
    def atualizar_status_atrasado(self):
        sql_update = """UPDATE emprestimos e
            SET id_disponibilidade = (
                SELECT id_disponibilidade
                FROM status_disponibilidade_produto
                WHERE descricao_disponibilidade = 'Em atraso'
            )
            WHERE e.id_disponibilidade = (
                SELECT id_disponibilidade
                FROM status_disponibilidade_produto
                WHERE descricao_disponibilidade = 'Emprestado'
            )
            AND e.data_devolucao < CURRENT_DATE; """
    
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_update)
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Erro ao atualizar atrasados: {e}")
        
    # DEVOLUCOES 
    '''def buscar_produtos_emprestados(conn):
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
    pass'''
    

class GerenciarAlteracoes:
    """Classe responsável por buscar dados sobre o empréstimo no banco de dados."""
    
    def __init__(self, conn):
        """Recebe uma conexão com o banco de dados."""
        self.conn = conn

    def adicionar_categoria(self, conn, categoria) -> bool:
        sql_insert = "INSERT INTO categorias_produto(nome_categoria) VALUES (%s)"

        try:
            with conn.cursor() as cur:
                cur.execute(sql_insert, (categoria, ))
            return True
        except ErroPsycopg2:
            raise ValueError ("Erro ao adicionar categoria!")
        except Exception:
            raise ValueError ("Erro inesperado ao adicionar categoria!")
    
    def adicionar_status(self, conn, status) -> bool:
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

    def adicionar_nome(self, nome, id_categoria) -> bool:
        sql_insert = "INSERT INTO nomes_produtos(nome_produto, id_categoria) VALUES (%s, %s)"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_insert, (nome, id_categoria ))
                return True
        except Exception:
            raise ValueError (MSG["erro_adicionar_nome"]["mensagem"])

    def alterar_status(self, conn, produto, status_antigo:str):
        id_status_novo = self.buscar_id_por_status(conn, produto.novo_status)
        id_prod = self.buscar_id_por_nomeCategoria_produto(conn, produto.nome, produto.categoria)
        id_status_antigo = self.buscar_id_por_status(conn, status_antigo)

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


class GerenciarGraficos:
    """Classe responsável por buscar dados para gerar gráficos na view."""
    
    def __init__(self, conn):
        """Recebe uma conexão com o banco de dados."""
        self.conn = conn

    def grafico_comparacao_ativos_inativos(self):
        sql_select = "SELECT * FROM vw_grafico_AtivoInativo"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_select)
                rows = cur.fetchall()
                if not rows or not rows[0]:
                    return {"Ativos": 0, "Inativos": 0}
                return {"Ativos": rows[0][0], "Inativos": rows[0][1]}
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
    def grafico_empCatDiarios(self):
        sql_select = "SELECT * FROM vw_grafico_empCatDia"
        try:
            resultados = []
            with self.conn.cursor() as cur:
                cur.execute(sql_select)
                rows = cur.fetchall()
                if not rows:
                    return resultados
                else:
                    for row in rows:
                        dicio = {"Categoria": row[0] or 0, "Qtd": row[1] or 0}
                        resultados.append(dicio)
                    return resultados
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")
        
    def grafico_itens_pendentesCat(self):
        sql_select = "SELECT * FROM vw_grafico_itenspencat"
        try:
            resultados = []
            with self.conn.cursor() as cur:
                cur.execute(sql_select)
                rows = cur.fetchall()
                if not rows:
                    return resultados
                else:
                    for row in rows:
                        dicio = {"Categoria": row[0] or 0, "Qtd": row[1] or 0}
                        resultados.append(dicio)
                    return resultados
        except Exception as e:
            raise ValueError (f"Erro inesperado ao realizar query: {e}")

    def atualizar_grafico(self):
        pass

    def atualizar_grafico_tempo(self):
        pass