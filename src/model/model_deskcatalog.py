# model.py
"""
Camada Model (Modelo):
- Define as classes de entidade (Produto, Empréstimo).
- Define as classes de acesso a dados (GerenciadorProduto).
- Define a lógica de negócios e cálculos (GerenciadorLanchonete, Calculos).
"""

from datetime import datetime as dt
import pytz

# ==================== CLASSES DE ENTIDADE ====================

#PODEMOS USAR ESSA CLASSE PARA SER NOSSO CATALOGO

class Produto:
    """Classe que representa um produto no sistema do catálogo"""

    """Recebe da view em string e depois para inserir no banco converte para o id"""
    def __init__(self, nome: str, categoria: str, quantidade: int, status: str):
        self.nome = nome.strip().title()
        self.categoria = categoria.strip().title()
        self.quantidade = quantidade
        self.status = status.strip().title()
        self.nu_patrimonio = None
        self.id_produto = None
        self.id_status = None

    def validar(self):
        if self.quantidade <= 0 or not isinstance(self.quantidade, int):
            raise ValueError ("Quantidade inválida!\n")
        if not self.nome or not self.nome.strip():
            raise ValueError ("Nome inválido!\n")
        if not self.categoria or not self.categoria.strip():
            raise ValueError ("Categoria inválida!\n")
        if not self.status.strip():
            raise ValueError ("Status inválido!\n")
        
    def produto_banco(self, id_produto, id_status):
        self.id_produto = id_produto
        self.id_status = id_status
        

class Emprestimo:
    """Classe que representa um emprestimo no sistema do catálogo"""

    tz = pytz.timezone('America/Sao Paulo')

    def __init__(self, nome_devolucao: str, nome_emprestimo: str, data_devolucao: str):
        self.id_emprestimo = None
        self.nu_patrimonio = None
        self.disponibilidade = None
        self.nome_devolucao = nome_devolucao.strip().title()
        self.nome_emprestimo = nome_emprestimo.strip().title()
        self.data_devolucao = data_devolucao.strip()
        self.devolveu_em = None
        self.data_emprestimo = None
        

    def validar(self):
        if not self.nome_devolucao:
            raise ValueError ("Nome do devolutor inválido.\n")
        if not self.nome_emprestimo:
            raise ValueError ("Nome do solicitador inválido.\n")
        
        data_datetime = self.data_devolucao_str_para_date()
        hoje = dt.now(self.tz).date()

        if data_datetime < hoje:
            raise ValueError ("A data não pode estar no passado.\n")
        
    # O DatePicker retorna string “YYYY-MM-DD”
    def data_devolucao_str_para_date(self) -> dt.date:
        return dt.strptime(self.data_devolucao, "%Y-%m-%d").date()
        
        
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
        
    def agora(self):
        return dt.now(self.tz)
    