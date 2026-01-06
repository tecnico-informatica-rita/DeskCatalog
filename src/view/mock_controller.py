class MockGerenciadorProduto:
    def __init__(self):
        self.categorias = ["Periféricos", "Móveis", "Áudio"]
        self.status = ["Ativo", "Inativo"]

        self.produtos = [
            {"categoria": "Móveis", "nome": "Cadeira Gamer", "total_produtos": 10, "total_disponiveis": 5, "total_ativo": 5},
            {"categoria": "Periféricos", "nome": "Teclado Mecânico", "total_produtos": 7, "total_disponiveis": 3, "total_ativo": 4},
            {"categoria": "Áudio", "nome": "Headset HyperX", "total_produtos": 4, "total_disponiveis": 2, "total_ativo": 2},
        ]

    def buscar_nome_categorias(self):
        return self.categorias

    def buscar_status(self):
        return self.status

    def buscar_nomes_produtos_existentes(self):
        return [p["nome"] for p in self.produtos]

    def adicionar_produto(self, prod):
        if not prod.nome or not prod.quantidade:
            return {"status": "erro", "mensagem": "Preencha todos os campos."}

        for p in self.produtos:
            if p["nome"].lower() == prod.nome.lower():
                p["total_produtos"] += int(prod.quantidade)
                p["total_ativo"] += int(prod.quantidade) if prod.status == "Ativo" else 0
                return {"status": "ok", "mensagem": "Quantidade atualizada!"}

        self.produtos.append({
            "categoria": prod.categoria,
            "nome": prod.nome,
            "total_produtos": int(prod.quantidade),
            "total_disponiveis": int(prod.quantidade),
            "total_ativo": int(prod.quantidade) if prod.status == "Ativo" else 0,
        })

        return {"status": "ok", "mensagem": "Produto cadastrado com sucesso!"}

    def exibir_todosP_qtd(self):
        return self.produtos

    def exibir_prod_disponiveis(self):
        return [
            {
                "categoria": p["categoria"],
                "nome": p["nome"],
                "total_produtos": p["total_produtos"],
                "total_disponiveis": p["total_disponiveis"],
            }
            for p in self.produtos
        ]


class MockController:
    def __init__(self):
        self.gerenciador_produto = MockGerenciadorProduto()

    def confimacao_usuario(self, emprestimo, nome_produto, categoria, qtd):
        qtd = int(qtd)
        for p in self.gerenciador_produto.produtos:
            if p["nome"] == nome_produto:
                if p["total_disponiveis"] == 0:
                    return {"status": "zerado"}
                if qtd <= p["total_disponiveis"]:
                    return {"status": "ok", "qtd": qtd, "pat": ["0001", "0002"]}
                return {"status": "insuficiente", "qtd": p["total_disponiveis"], "pat": ["0001", "0002"]}
        return {"status": "erro", "msg": "Produto não encontrado"}

    def fazer_emprestimo(self, emprestimo, qtd, pat):
        return {"status": "sucesso", "qtd_registrada": qtd}