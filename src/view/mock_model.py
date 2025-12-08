class Emprestimo:
    def __init__(self, nome_emprestimo, data_devolucao):
        self.nome_emprestimo = nome_emprestimo
        self.data_devolucao = data_devolucao

class Produto:
    def __init__(self, nome, categoria, quantidade, status):
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.status = status