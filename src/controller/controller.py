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

  def adicionar_produto_existente(self, produto: model.Produto):
    produto.validar()

    
    



