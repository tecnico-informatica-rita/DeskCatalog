

import flet as ft

'''from database.database_banco import get_db_connection # ajuste se o nome for outro
from model.model_deskcatalog import GerenciarGraficos
from view.home_modular.dashboard import HomeDashboard


def main(page: ft.Page):
    page.title = "Teste Dashboard - Banco Real"
    page.window_width = 1300
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # ===== CONEXÃO REAL =====
    conn = get_db_connection()

    dashboard = HomeDashboard(
        conn=conn,
        model=GerenciarGraficos(conn),
    )

    page.add(dashboard.build(page))


if __name__ == "__main__":
    ft.app(target=main)'''

'''import flet as ft

from database.database_banco import get_db_connection
from view.home_modular.home_redesenhada import HomeView
from view.home_modular.navegacao import criar_navigation

def main(page: ft.Page):
    # ===== CONFIGURAÇÕES BÁSICAS =====
    page.title = "DeskCatalog"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    # ===== CONEXÃO REAL COM O BANCO =====
    conn = get_db_connection()

    # ===== HOME VIEW =====
    appbar, drawer = criar_navigation(page)

    page.appbar = appbar
    page.drawer = drawer
    home = HomeView(conn)

    # Limpa a página e monta a Home
    #page.controls.clear()
    page.add(home.build(page))

    page.update()


if __name__ == "__main__":
    ft.app(
        target=main, assets_dir="assets",
        #view=ft.AppView.WEB_BROWSER  # ou FLET_APP se usar desktop
    )'''

# main.py
'''from database.database_banco import get_db_connection
from view.home_modular.home_redesenhada import HomeView
from view.home_modular.navegacao import criar_navigation


def main(page: ft.Page):
    # Configurações
    page.title = "DeskCatalog"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = None

    conn = get_db_connection()

    # 1. Primeiro defina o conteúdo
    home = HomeView(conn)
    conteudo = home.build(page)

# 2. Adicione o conteúdo à página
    page.add(conteudo)

# 3. SÓ DEPOIS crie e defina o AppBar e o Drawer
# Isso força o sistema a desenhar a barra de navegação POR CIMA do conteúdo
    appbar, drawer = criar_navigation(page)
    page.appbar = appbar
    page.drawer = drawer

    page.update()

import flet as ft
from view.home_modular.home_redesenhada import HomeView
from view.home_modular.navegacao import criar_navigation
from database.database_banco import get_db_connection


if __name__ == "__main__":
    ft.app(
        target=main, assets_dir="assets",
        #view=ft.AppView.WEB_BROWSER  # ou FLET_APP se usar desktop
    )'''

import flet as ft
from database.database_banco import get_db_connection
from view.home_modular.home_redesenhada import HomeView

def main(page: ft.Page):
    # Configurações iniciais da página
    page.title = "DeskCatalog"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = None

    # Conexão com o banco
    conn = get_db_connection()

    # Cria a Home
    home = HomeView(conn)

    # Chama o método que monta a Home COMPLETA (layout + AppBar + Drawer)
    home.main_home(page)

if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
        # view=ft.AppView.WEB_BROWSER  # ou FLET_APP se for desktop
    )


