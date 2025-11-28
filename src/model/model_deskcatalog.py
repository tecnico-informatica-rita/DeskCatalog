# model.py
"""
Camada Model (Modelo):
- Define as classes de entidade (Produto, Empréstimo).
- Define as classes de acesso a dados (GerenciadorProduto).
- Define a lógica de negócios e cálculos (GerenciadorLanchonete, Calculos).
"""

# ==================== CLASSES DE ENTIDADE ====================

#PODEMOS USAR ESSA CLASSE PARA SER NOSSO CATALOGO

class Produto:
    """Classe que representa um produto no sistema do catálogo"""

    """Recebe da view em string e depois para inserir no banco converte para o id"""
    def __init__(self, nome: str, categoria: str, quantidade: int, status: str):
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.status = status
        self.nu_patrimonio = None
        self.id_produto = None

    def validar(self):
        if self.quantidade <= 0 or not isinstance(self.quantidade, int):
            raise ValueError ("Quantidade inválida!")
        if not self.nome or not self.nome.strip():
            raise ValueError ("Nome inválido!")
        if not self.categoria or not self.categoria.strip():
            raise ValueError ("Categoria inválida!")
        if not self.status.strip():
            raise ValueError ("Status inválido!")



class Emprestimo:
    """Classe que representa um emprestimo no sistema do catálogo"""

    def __init__(self, nome_devolucao, nome_emprestimo, data_devolucao):
        self.id_emprestimo = None
        self.nu_patrimonio = None
        self.disponibilidade = None
        self.nome_devolucao = nome_devolucao
        self.nome_emprestimo = nome_emprestimo
        self.data_devolucao = data_devolucao
        self.devolveu_em = None
        self.data_emprestimo = None
        

    def validar(self):
        pass
