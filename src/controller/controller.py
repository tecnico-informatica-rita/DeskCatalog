# controller.py
"""
Camada Controller (Controle):
- Orquestra o fluxo da aplicação.
- Recebe inputs da View, processa-os (valida), chama o Model
  para lógica de negócios ou dados, e envia os resultados para a View.
- Gerencia o estado da aplicação (ex: o carrinho).
"""

import model.model_deskcatalog as model
import view.view as view
import database.database_funcoes as db


class ControllerDeskCatalog:
  """Interliga o model ao banco de dados e a view"""
  
  def __init__(self, conn):
      """Inicializa o controlador com os gerenciadores do modelo."""
      self.conn = conn
      self.view = view # Referência para o módulo da View
      self.gerenciador_produto = model.GerenciadorProduto(conn)
      self.gerenciador_emprestimo = model.GerenciarEmprestimo(conn)
      self.gerenciador_alteracoes = model.GerenciarAlteracoes(conn)
    

  # ==================== FUNÇÕES DE VALIDAÇÃO (LÓGICA DO CONTROLE) ====================

  def validar_nomeCategoria(self, produto):
    id_prod = db.buscar_id_por_nomeCategoria_produto(self.conn, produto.nome, produto.categoria)
    if not id_prod:
      raise ValueError ("Esse item não existe no catálogo.")
    return id_prod
  
  def validar_status(self, produto):
    id_status = db.buscar_id_por_status(self.conn, produto.status)
    if not id_status:
      raise ValueError ("Esse status não existe no catálogo.")
    return id_status
  
  def validar_categoria(self, produto):
    id_categoria = db.buscar_id_por_categoria(self.conn, produto.categoria)
    if not id_categoria:
      raise ValueError ("Essa categoria não existe no catálogo.")
    return id_categoria


  # ==================== FUNÇÕES DE PROCESSAMENTO (AÇÕES DO MENU) ====================

  def adicionar_produto_existente(self, produto: model.Produto) -> bool:
    # Validação do produto antes de inserir
    produto.validar()
    
    # Verificando se esse produto existe no banco
    id_prod = self.validar_nomeCategoria(produto)
    id_status = self.validar_status(produto)
    
    # Inserção do produto no banco
    if id_prod and id_status:
      produto.produto_banco(id_prod, id_status) # Substituição dos atributos pelo ID
      db.inserir_varios_produtos_iguais(self.conn, produto)
      return True
    else:
      raise ValueError ("Informações inválidas para cadastrar item.\n")
    


  def adicionar_produto_novo(self, produto: model.Produto) -> bool:
    # Validação do produto antes de inserir
    produto.validar()
    
    # Verificando que não existe esse produto no banco
    id_prod = self.validar_nomeCategoria(produto)
    if id_prod:
      raise ValueError ("Esse produto já existe no catálogo.\n")
    
    id_status = self.validar_status(produto)
    if not id_status:
      raise ValueError (f"Erro: O Status '{produto.status}' não foi encontrado no catálogo.")
    
    id_categoria = self.validar_categoria(produto)
    if not id_categoria:
      raise ValueError (f"Erro: A Categoria '{produto.categoria}' não foi encontrada no catálogo.")
    
    # Adicionando no banco a categoria, o status e o nome
    try:
        db.adicionar_nome(self.conn, produto.nome, id_categoria)
        id_prod = self.validar_nome(produto)
        if id_prod:
          produto.produto_banco(id_prod, id_status)
          db.inserir_varios_produtos_iguais(self.conn, produto)
          return True
        else:
          raise ValueError ("Erro interno: Falha ao confirmar o ID do produto recém-cadastrado.")
    except Exception as e:
      raise ValueError (f"Erro inesperado durante a persistência de dados: {e}")
    

  def alterar_dados_produto(self, ):
    pass


  def exibir_todos_produtos(self,):
    resultados = db.exibir_todos_produtos(self.conn)

    lista = []
    for i in resultados:
      resultado_dict = {
        'patrimonio': i[0],
        'categoria': i[1],
        'nome': i[2],
        'status': i[3]
      }
      lista.append(resultado_dict)

      return lista
    

#       REALIZANDO EMPRÉSTIMOS

  def fazer_emprestimo(self, emprestimo, nome, categoria, qtd):
    qtd_banco, pat_validos = db.validar_nu_patrimonio(self.conn, nome, categoria, qtd)

    if qtd_banco is True:
      qtd_emprestada = qtd
      pat_emprestados = pat_validos
    else:
      qtd_disponivel = len(pat_validos)
      confirmacao =  'Função que a view vai retornar'
      if confirmacao is True:
        qtd_emprestada = qtd_disponivel
        pat_emprestados = pat_validos
      else:
        return {"status": "cancelado", "mensagem": "Empréstimo cancelado pelo usuário."}
      
    emprestado, qtd_emprestimos = db.realizar_emprestimo(self.conn, emprestimo, qtd_emprestada, pat_emprestados)
    return {"status": "sucesso", "qtd_registrada": qtd_emprestimos}


    
  def fazer_devolucao(self,):
    pass

  # ==================== LOOP PRINCIPAL DA APLICAÇÃO ====================

  def run(self):
    """Função principal que executa o sistema."""
    pass
    
    



