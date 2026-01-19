import flet as ft
from view.home_modular.navegacao import criar_navigation
import database.database_banco as database
from view.rotas2 import gerenciar_rotas  # importando o gerenciador de rotas

def main(page: ft.Page):
    # Configurações iniciais
    page.title = "DeskCatalog"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = None

    conn = database.get_db_connection()
    database.criar_tabelas(conn)
    database.popular_dados_padrao(conn)

    # Configura o sistema de rotas
    page.on_route_change = gerenciar_rotas(page, conn)
    page.go("/")  # inicia na Home

    # Cria o Drawer e AppBar
    appbar, drawer = criar_navigation(page)
    page.appbar = appbar
    page.drawer = drawer

    page.update()


if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
        # view=ft.AppView.WEB_BROWSER  # ou FLET_APP se for desktop
    )
