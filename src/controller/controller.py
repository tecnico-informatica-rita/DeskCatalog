# controller.py
"""
Camada Controller (Controle):
- Orquestra o fluxo da aplicação.
- Recebe inputs da View, processa-os (valida), chama o Model
  para lógica de negócios ou dados, e envia os resultados para a View.
- Gerencia o estado da aplicação (ex: o carrinho).
"""
import src.view.view as view
from src.model.model import pegar_linhas_da_view_do_banco, separar_o_retorno_por_variavel

def dividir_retorno_por_variavel(nome_view):
    try:
      pegar_linhas_banco = pegar_linhas_da_view_do_banco(nome_view)
      resultado = separar_o_retorno_por_variavel(pegar_linhas_banco)
      return resultado

    except Exception as e:
      return "Algum erro inesperado aconteceu: {e}"

print(dividir_retorno_por_variavel('visao_informatica'))