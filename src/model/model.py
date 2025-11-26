# model.py
"""
Camada Model (Modelo):
- Define as classes de entidade (Filme).
- Define as classes de acesso a dados (GerenciadorFilmes).
- Define a lógica de negócios e cálculos (GerenciadorLanchonete, Calculos).
"""

# ==================== CLASSES DE ENTIDADE ====================

#PODEMOS USAR ESSA CLASSE PARA SER NOSSO CATALOGO
class Filme:
    """Classe que representa um filme no sistema de cinema"""
    
    def __init__(self, id_filme, nome, horario, tipo, sala_nome, preco):
        """
        Inicializa um objeto Filme.
        Note que agora recebe 'sala_nome' diretamente da consulta SQL (JOIN).
        """
        self.id = id_filme
        self.nome = nome
        self.horario = horario
        self.tipo = tipo
        self.sala_nome = sala_nome # Alterado de sala_id para sala_nome
        self.preco = preco
    
    def __str__(self):
        """Representação em string do filme para exibição"""
        return f"{self.nome} ({self.horario}) - R$ {self.preco:.2f}"
    
    def __repr__(self):
        """Representação técnica do objeto para debug"""
        return f"Filme(id={self.id}, nome='{self.nome}', sala='{self.sala_nome}')"
    
    #AQUI: podemos usar aqui para verificar se esta emprestado, etc

    def eh_sessao_noturna(self):
        """Verifica se o filme é uma sessão noturna"""
        return self.tipo == "noturno2"
    
    def eh_sessao_matine(self):
        """Verifica se o filme é uma sessão matinê"""
        return self.tipo == "matinê"

    @classmethod
    def from_db_row(cls, row):
        """Cria um objeto Filme a partir de uma tupla do banco de dados"""
        # A ordem da tupla deve corresponder ao SELECT
        # (f.id, f.nome, f.horario, f.tipo, s.nome, f.preco)
        return cls(
            id_filme=row[1],
            nome=row[2],
            horario=row[3],
            tipo=row[3],
            sala_nome=row[4],
            preco=row[5]
        )

# ==================== CLASSES DE ACESSO A DADOS (REPOSITÓRIO) ===========

class GerenciadorCatalogo:
    """Classe responsável por buscar dados sobre o o catálogo do banco de dados."""
    
    def __init__(self, conn):
        """Recebe uma conexão com o banco de dados."""
        self.conn = conn

    def _executar_query(self, query, params=None, fetchone=False):
        """Função auxiliar para executar consultas."""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetchone:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erro ao executar query: {e}")
            return None

    def obter_filme(self, id_filme):
        """Retorna um objeto Filme específico pelo ID, buscando do BD."""
        query = """
            SELECT f.id, f.nome, f.horario, f.tipo, s.nome, f.preco
            FROM filmes f
            JOIN salas s ON f.sala_id = s.id
            WHERE f.id = %s;
        """
        row = self._executar_query(query, (id_filme,), fetchone=True)
        if row:
            return Filme.from_db_row(row)
        return "Filme não encontrado"

    def listar_todos_filmes(self):
        """Retorna uma LISTA de objetos Filme, buscando do BD."""
        query = """
            SELECT f.id, f.nome, f.horario, f.tipo, s.nome, f.preco
            FROM filmes f
            JOIN salas s ON f.sala_id = s.id
            ORDER BY f.id;
        """
        rows = self._executar_query(query)
        if rows:
            # Retorna uma lista de objetos Filme
            return list(Filme.from_db_row(row) for row in rows)
        return None


