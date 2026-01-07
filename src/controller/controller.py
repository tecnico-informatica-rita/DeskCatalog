# controller.py

import model.model_deskcatalog as model
from model.model_deskcatalog import MSG
import database.database_banco as db

"""
Camada Controller (Controle):
- Orquestra o fluxo da aplicação.
- Recebe inputs da View, processa-os (valida), chama o Model
  para lógica de negócios ou dados, e envia os resultados para a View.
- Gerencia o estado da aplicação (ex: o carrinho).
"""

class ControllerDeskCatalog:
  """Interliga o model ao banco de dados e a view"""
  
  def __init__(self, conn):
      """Inicializa o controlador com os gerenciadores do modelo."""
      self.conn = conn
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
      id_status = self.gerenciador_produto.buscar_id_por_status(produto.status)
      if not id_status:
        raise ValueError (MSG["erro_status_invalido"]["mensagem"])
      return id_status
    
  def validar_categoria(self, produto):
      id_categoria = self.gerenciador_produto.buscar_id_por_categoria( produto.categoria)
      if not id_categoria:
        raise ValueError (MSG["erro_categoria_invalida"]["mensagem"])
      return id_categoria

  
  # ==================== FUNÇÕES DE PROCESSAMENTO (AÇÕES DO MENU) ====================

  # Cadastrar itens ---------------------------------------------------------------------------------------------------------
  def adicionar_produto_existente(self, id_prod, produto: model.Produto):
    id_status = self.validar_status(produto)
    produto.produto_banco(id_prod, id_status) 
    self.gerenciador_produto.inserir_varios_produtos_iguais(produto)


  def adicionar_produto_novo(self, produto: model.Produto, id_categoria: int):
    self.gerenciador_alteracoes.adicionar_nome(produto.nome, id_categoria)
    dados_novo_prod = self.gerenciador_produto.buscar_dados_produto_por_nome(produto.nome)
    
    if not dados_novo_prod:
        raise ValueError(MSG["erro_id_interno"]["mensagem"])
    
    id_prod = dados_novo_prod['id_produto']
    id_status = self.validar_status(produto)

    produto.produto_banco(id_prod, id_status)
    self.gerenciador_produto.inserir_varios_produtos_iguais(produto)


  def adicionar_produto(self, produto: model.Produto) -> dict:
    try:
      produto.validar()
      id_categoria = self.validar_categoria(produto)
        
      dados_existentes = self.gerenciador_produto.buscar_dados_produto_por_nome(produto.nome)
        
      if dados_existentes: 
          id_prod_existente = dados_existentes['id_produto']
          id_cat_registrada = dados_existentes['id_categoria']
            
          if id_cat_registrada == id_categoria:
            self.adicionar_produto_existente(id_prod_existente, produto)
            return MSG["sucesso_add_qtd"]
          else:
            raise ValueError (MSG["erro_ja_cadastrado_outraC"]["mensagem"]) 
      else:
        self.adicionar_produto_novo(produto, id_categoria)
        return MSG["sucesso_add_prod"]

    except ValueError as e:
      raise ValueError(str(e))
    except Exception:
        raise ValueError(MSG["erro_geral"]["mensagem"])
  

  # Exibição necessária para a função 'Cadastrar' -------------------------------------------------------------------------------
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
    

  # Realizar empréstimos --------------------------------------------------------------------------------------------------------
  def confimacao_usuario(self, emprestimo, nome, categoria, qtd):
    self.gerenciador_emprestimo.atualizar_status_atrasado()
    emprestimo.validar()
    qtd_banco, pat_validos = self.gerenciador_emprestimo.validar_nu_patrimonio( nome, categoria, qtd)

    if len(pat_validos) == 0:
        return {"status": "zerado", "qtd": 0, "pat": []}
    
    if qtd_banco is True:
      return {"status": "ok", "qtd": qtd, "pat": pat_validos}
    
    if not qtd_banco or len(pat_validos) < qtd:
        qtd_disponivel = len(pat_validos)
        return {"status": "insuficiente", "qtd": qtd_disponivel, "pat": pat_validos}
      
  def fazer_emprestimo(self, emprestimo, qtd, pat_validos):
    emprestado, qtd_emprestimos = self.gerenciador_emprestimo.realizar_emprestimo( emprestimo, qtd, pat_validos)
    return {"status": "sucesso", "qtd_registrada": qtd_emprestimos}

  # Exibição necessária para a função 'Empréstimo' -------------------------------------------------------------------------------
  def exibir_prod_disponiveis(self,):
    resultados = self.gerenciador_emprestimo.exibir_produtos_disponiveis()

    lista = []
    for i in resultados:
      resultado_dict = {
        'categoria': i[0],
        'nome': i[1],
        'total_produtos': i[2],
        'total_disponiveis': i[3]
      }
      lista.append(resultado_dict)

    return lista
  
 
  # Realizar devoluções (NÃO FINALIZADA) ----------------------------------------------------------------------------------------------------------
  
  #def fazer_devolucao(self, id_produto, categoria, qtd):
    #return self.gerenciador_emprestimo.realizar_devolucao(id_produto, categoria, qtd)
  
  def confirmacao_usuario_devolucao(self, emprestimo, nome_produto, qtd):
    emprestimo.validar()

    # Verificar patrimônios emprestados pelo usuário
    qtd_banco, pat_validos = self.gerenciador_emprestimo.validar_nuP_total(nome_produto, emprestimo, qtd)

    # Nenhum para devolver
    if not pat_validos:
        return {"status": "zerado", "qtd": 0, "pat": []}

    # Tem todos os itens
    if qtd_banco is True:
        return {"status": "ok", "qtd": qtd, "pat": pat_validos}

    # Tem só parte deles -> devolução parcial
    if not qtd_banco or len(pat_validos) < qtd:
        qtd_disponivel = len(pat_validos)
        return {"status": "insuficiente", "qtd": qtd_disponivel, "pat": pat_validos}
      
  def fazer_devolucao(self, emprestimo, qtd, pat_validos):
    emprestado, qtd_devolvida = self.gerenciador_emprestimo.realizar_devolucao( emprestimo, qtd, pat_validos)
    return {"status": "sucesso", "qtd_registrada": qtd_devolvida}
  

  # Exibição necessária para a função 'Empréstimo' -------------------------------------------------------------------------------
  def exibir_prod_devolucao(self,):
    resultados = self.gerenciador_emprestimo.exibir_devolucoes()

    lista = []
    for i in resultados:
      resultado_dict = {
        'categoria': i[0],
        'produto': i[1],
        'nome_emprestimo': i[2],
        'data_emprestimo': i[3],
        'disponibilidade': i[4],
        'qtd': i[5],
      }
      lista.append(resultado_dict)

    return lista




# =======================================================================================================
# =============================================== PARTE DA ANA ==========================================
# =======================================================================================================



from model.model_deskcatalog import pegar_linhas_da_view_do_banco, separar_o_retorno_por_variavel, separar_o_retorno_por_variavel_relatorio_30_dias, separar_o_retorno_por_variavel_historico_de_transaces
from model.model_deskcatalog import enviar_email, Autenticar_senha

def dividir_retorno_por_variavel(conn, nome_view):
    try:
      pegar_linhas_banco = pegar_linhas_da_view_do_banco(conn, nome_view)
      resultado = separar_o_retorno_por_variavel(pegar_linhas_banco)
      return resultado

    except Exception as e:
      return "Algum erro inesperado aconteceu: {e}"


def autenticar_loguin_completo(usuario, senha):
    """
    Retorna True se:
    email for enviado com sucesso
    senha validada
    """
    try:
        email_ok = enviar_email(usuario)
        senha_ok = Autenticar_senha(senha)
        if email_ok and senha_ok:
            return True
        else:
            return False

    except Exception as e:
        print("Erro ao autenticar:", e)
        return False

def mostrar_informaçoes_dos_ultimos_30_dias(conn):
    try:
        lista = pegar_linhas_da_view_do_banco(conn, 'visao_itens_para_devolucao_30_dias')
        print("DEBUG consulta view:", lista) 

        resultado = separar_o_retorno_por_variavel_relatorio_30_dias(lista)
        print("DEBUG dicionarios:", resultado)

        return resultado

    except Exception as e:
        return f"um erro inesperado aconteceu: {e}"
    
def mostrar_historico_transacoes_de_emprestimo(conn):
    try:
        lista = pegar_linhas_da_view_do_banco(conn, 'visao_historico_transacoes_emprestimos')
        resultado = separar_o_retorno_por_variavel_historico_de_transaces(lista)
        return resultado
    
    except Exception as e:
        return f"um erro inesperado aconteceu: {e}"
  
