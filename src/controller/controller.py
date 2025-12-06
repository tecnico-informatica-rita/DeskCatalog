# controller.py
"""
Camada Controller (Controle):
- Orquestra o fluxo da aplicação.
- Recebe inputs da View, processa-os (valida), chama o Model
  para lógica de negócios ou dados, e envia os resultados para a View.
- Gerencia o estado da aplicação (ex: o carrinho).
"""

import model.model_deskcatalog as model
from model.model_deskcatalog import MSG
import view_cadastro as view
import database.database_banco as db



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
    try:
      id_prod = self.gerenciador_produto.buscar_id_por_nomeCategoria_produto(produto.nome, produto.categoria)
      return id_prod
    except Exception as e:
      raise ValueError (f"Erro inesperado durante a busca pelo produto válido: {e}")
  
  def validar_status(self, produto):
    try:
      id_status = self.gerenciador_produto.buscar_id_por_status(produto.status)
      if not id_status:
        raise ValueError ("Esse status não existe no catálogo.")
      return id_status
    except Exception as e:
      raise ValueError (f"Erro inesperado durante a busca pelo status: {e}")
  
  def validar_categoria(self, produto):
    try:
      id_categoria = self.gerenciador_produto.buscar_id_por_categoria( produto.categoria)
      if not id_categoria:
        raise ValueError ("Essa categoria não existe no catálogo.")
      return id_categoria
    except Exception as e:
      raise ValueError (f"Erro inesperado durante a busca pela categoria: {e}")


  # ==================== FUNÇÕES DE PROCESSAMENTO (AÇÕES DO MENU) ====================

  def adicionar_produto_existente(self, produto: model.Produto) -> bool:
    # Validação do produto antes de inserir
    produto.validar()
    
    # Verificando se esse produto existe no banco
    id_prod = self.validar_nomeCategoria(produto)
    id_status = self.validar_status(produto)
    
    # Inserção do produto no banco
    if id_prod is not None and id_status:
      produto.produto_banco(id_prod, id_status) # Substituição dos atributos pelo ID
      self.gerenciador_produto.inserir_varios_produtos_iguais(produto)
      return True
    
    if id_prod is None:
        raise ValueError (MSG["erro_ja_cadastrado_outraC"]["mensagem"])
    
    raise ValueError ("Informações inválidas para cadastrar item.\n")
    
  

  def adicionar_produto_novo(self, produto: model.Produto) -> bool:
    # Validação do produto antes de inserir
    produto.validar()
    
    # Verificando que não existe esse produto no banco
    id_prod = self.validar_nomeCategoria(produto)
    if id_prod:
      raise ValueError (MSG["erro_ja_cadastrado"]["mensagem"])
    
    id_status = self.validar_status(produto)
    id_categoria = self.validar_categoria(produto)

    '''if not id_status:
      raise ValueError (f"Erro: O Status '{produto.status}' não foi encontrado no catálogo.")
    
    
    if not id_categoria:
      raise ValueError (f"Erro: A Categoria '{produto.categoria}' não foi encontrada no catálogo.")'''
    
    # Adicionando no banco a categoria, o status e o nome

    self.gerenciador_alteracoes.adicionar_nome( produto.nome, id_categoria)

    id_prod = self.validar_nome(produto)
    if not id_prod:
      raise ValueError ("Erro interno: Falha ao confirmar o ID do produto recém-cadastrado.")
    
    produto.produto_banco(id_prod, id_status)
    self.gerenciador_produto.inserir_varios_produtos_iguais(produto)
    return True
        

  def adicionar_produto(self, prod):
    """ Se o produto existir → adiciona quantidade.
        Se não existir → cadastra como um novo item.
    """
    try:
      self.adicionar_produto_existente(prod)
      return MSG["sucesso_add_qtd"]
    except ValueError as e:
      erro = str(e).lower()

      if "não existe no catálogo" in erro or "esse item não existe" in erro:
        self.adicionar_produto_novo(prod)
        return MSG["sucesso_add_prod"]
    
      raise ValueError(str(e))
    
  def alterar_dados_produto(self, ):
    pass


  def exibir_todos_produtos(self,):
    resultados = self.gerenciador_produto.exibir_todos_produtos()

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
    
  def exibir_todosP_qtd(self,):
    resultados = self.gerenciador_produto.exibir_todos_produtos_qtdAtivos()

    lista = []
    for i in resultados:
      resultado_dict = {
        'categoria': i[0],
        'nome': i[1],
        'total_produtos': i[2],
        'total_ativo': i[3]
      }
      lista.append(resultado_dict)

    return lista
    
#       REALIZANDO EMPRÉSTIMOS

  def fazer_emprestimo(self, emprestimo, nome, categoria, qtd):
    qtd_banco, pat_validos = self.gerenciador_emprestimo.validar_nu_patrimonio(self.conn, nome, categoria, qtd)

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
      
    emprestado, qtd_emprestimos = self.gerenciador_emprestimo.realizar_emprestimo(self.conn, emprestimo, qtd_emprestada, pat_emprestados)
    return {"status": "sucesso", "qtd_registrada": qtd_emprestimos}


    
  def fazer_devolucao(self,):
    pass

  # ==================== LOOP PRINCIPAL DA APLICAÇÃO ====================

  def run(self):
    """Função principal que executa o sistema."""
    pass
    
    



