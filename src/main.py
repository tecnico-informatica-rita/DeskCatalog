# main.py LIMPEZA FEITA

"""
Ponto de entrada principal do projeto.

- orquestra todos os arquivos e eventos.

Responsabilidades:
1. Importar os módulos da aplicação.
2. Estabelecer a conexão inicial com o banco de dados.
3. Chamar a inicialização do banco (criar tabelas, popular dados).
4. Instanciar o Controlador (Controller).
5. Iniciar o loop principal da aplicação.
6. Gerenciar o fechamento da conexão com o banco.
"""

import flet as ft
import database.database_banco as database   # Para setup e conexão
import controller.controller as controller   # O cérebro da aplicação
from view.cadastro import cadastro_view
from view.emprestimo import emprestimo_view
from view.devolucao import devolucao_view

# testando a view das meninas
from view.home_modular.home import home_view

#from view.home.home import home_view as hw

import sys            # Para encerrar o programa em caso de erro de DB

'''def main(page: ft.Page):
    """Função principal que configura e executa o sistema."""
    
    conn = None
    try:
        # 1. Conectar ao banco de dados
        print("ℹ️  Conectando ao banco de dados PostgreSQL...")
        conn = database.get_db_connection()
        print("✅ Conexão estabelecida.")
        
        # 2. Garantir que tabelas e dados existam
        print("ℹ️  Verificando estrutura do banco de dados...")
        database.criar_tabelas(conn)
        database.popular_dados_padrao(conn)
        print("✅ Banco de dados pronto.")
        
        # 3. Instanciar e executar o controlador
        # O controlador recebe a conexão para passar aos seus gerenciadores
        #app = controller.ControllerDeskCatalog(conn)

        #page.add(pagina_emprestimo(app, page))
        #app.run()
        #view = cadastro_view(conn)
        #page.add(view.main_cadastro(page))

        #view = emprestimo_view(conn)
        #page.add(view.main_emprestimo(page))
        
        #page.add(devolucao_view(conn))

        #view = devolucao_view(conn)
        #page.add(view.main_devolucao(page))

        view = home_view(conn)
        page.add(view.main_home(page))

    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado na aplicação: {e}")
    
    finally:
        # 4. Fechar a conexão ao sair
        if conn:
            conn.close()
            print("ℹ️  Conexão com o banco de dados fechada.")

#if __name__ == "__main__":
    #main()

ft.app(target=main)'''


#  PARTE DA ANA -----------------------------------------------------------------------------------------------------------------
import flet as ft
from view.ROTAS import gerenciar_rotas
conn = database.get_db_connection()
print("✅ Conexão estabelecida.")
        
        # 2. Garantir que tabelas e dados existam
print("ℹ️  Verificando estrutura do banco de dados...")
database.criar_tabelas(conn)
database.popular_dados_padrao(conn)
print("✅ Banco de dados pronto.")
        
def main(page: ft.Page):
    conn = database.get_db_connection()
    page.on_route_change = gerenciar_rotas(page, conn)
    page.go(page.route)

ft.app(target=main)

