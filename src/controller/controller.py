# controller.py
"""
Camada Controller (Controle):
- Orquestra o fluxo da aplicação.
- Recebe inputs da View, processa-os (valida), chama o Model
  para lógica de negócios ou dados, e envia os resultados para a View.
- Gerencia o estado da aplicação (ex: o carrinho).
"""

import src.model.model as model
import src.view.view as view
import src.database.database_deskcatalog as db


class ControllerProduto:
  """Interliga o produto ao banco de dados e a view"""
  
  def __init__(self, conn):
    self.conn = conn

  def validar_produto_banco(self, produto):
    nomes_produtos = db.buscar_nomes_produtos_existentes(self.conn)
    nomes_categorias = db.buscar_nome_categorias(self.conn)
    status = db.buscar_status(self.conn)

    if not produto.nome in nomes_produtos:
      raise ValueError ("Esse item não existe no catálogo.")
    
    if not produto.categoria in nomes_categorias:
      raise ValueError ("Essa categoria não existe no catálogo.")

    if not produto.status in status:
      raise ValueError ("Esse status não existe no catálogo.")


  def adicionar_produto_existente(self, produto: model.Produto) -> bool:
    # Validação do produto antes de inserir
    produto.validar()
    self.validar_produto_banco(produto)

    # Substituição dos nomes pelo ID
    id_prod = db.buscar_id_por_nome_produto(self.conn, produto.nome)
    id_status = db.buscar_id_por_status(self.conn, produto.status)

    # Inserção do produto no banco
    if id_prod and id_status:
      produto.produto_banco(id_prod, id_status)
      db.inserir_varios_produtos_iguais(self.conn, produto)
    else:
      raise ValueError ("Informações inválidas para cadastrar item.\n")
    

  def adicionar_produto_novo(self, produto: model.Produto) -> bool:
    pass

    
    
    



