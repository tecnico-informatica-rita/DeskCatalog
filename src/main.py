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

import src.database.database as database   # Para setup e conexão
import src.controller.controller as controller   # O cérebro da aplicação
import sys            # Para encerrar o programa em caso de erro de DB

import flet as ft
from src.view.ROTAS import gerenciar_rotas

def main(page: ft.Page):
    page.on_route_change = gerenciar_rotas(page)
    page.go(page.route)

ft.app(target=main)