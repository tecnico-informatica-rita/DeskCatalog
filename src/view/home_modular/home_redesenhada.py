import flet as ft
from header import home_header
from categorias import home_categories

'''class HomeView:
    def __init__(self, conn):
        self.conn = conn

    def build(self, page: ft.Page):
        page.title = "Home"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        return ft.Column(
            controls=[
                home_header(),
                home_categories(),
                # depois entra: home_charts()
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )'''

import flet as ft
from header import home_header
from categorias import home_categories
from navegacao import criar_navigation


class HomeView:
    def __init__(self, conn):
        self.conn = conn

    def _on_search(self, texto):
        print("Pesquisando por:", texto)
        # depois:
        # page.go(f"/resultado?query={texto}")
        
    def build(self, page: ft.Page):
        # ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
        page.title = "Home"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        # ---------------- NAVIGATION ----------------
        appbar, drawer = criar_navigation(page)
        page.appbar = appbar
        page.drawer = drawer

        # ---------------- CONTEÚDO DA HOME ----------------
        return ft.Column(
            controls=[
                home_header(),
                home_categories(),
                # depois entra: home_charts(self.conn)
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

