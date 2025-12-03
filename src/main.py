# main.py
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

import database.database_banco as database   # Para setup e conexão
import controller.controller as controller   # O cérebro da aplicação
import sys            # Para encerrar o programa em caso de erro de DB

def main():
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
        #app = controller.SistemaCinema(conn)
        #app.run()
        
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado na aplicação: {e}")
    
    finally:
        # 4. Fechar a conexão ao sair
        if conn:
            conn.close()
            print("ℹ️  Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()