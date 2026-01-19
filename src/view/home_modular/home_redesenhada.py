import flet as ft

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

'''import flet as ft
from view.home_modular.header import home_header
from view.home_modular.categorias import home_categories
from view.home_modular.navegacao import criar_navigation
from view.home_modular.dashboard import HomeDashboard
from model.model_deskcatalog import GerenciarGraficos


class HomeView:
    def __init__(self, conn):
        self.conn = conn
        self.dashboard = HomeDashboard(self.conn, GerenciarGraficos(conn))

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
        
        # ---------------- CONTEÚDO DA HOME ----------------
        return ft.Column(
            controls=[
                home_header(),
                self.dashboard.build(page),
                home_categories(),
                # depois entra: home_charts(self.conn)
            ],
            expand=False,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )'''


import flet as ft
from view.home_modular.header import home_header
from view.home_modular.categorias import home_categories
from view.home_modular.dashboard2 import HomeDashboard
from model.model_deskcatalog import GerenciarGraficos

# HOME CERTA
'''class HomeView:
    def __init__(self, conn):
        self.conn = conn
        self.dashboard = HomeDashboard(self.conn, GerenciarGraficos(conn))

    def _on_search(self, texto):
        print("Pesquisando por:", texto)
        # depois você pode navegar:
        # page.go(f"/resultado?query={texto}")

    def build(self, page: ft.Page):
        # ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
        page.title = "Home"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        # ---------------- CONTEÚDO DA HOME ----------------
        # ⚡ Coluna principal sem expand, com scroll automático
        return ft.Column(
            controls=[
                # Header fixo no topo
                home_header(on_search=self._on_search),

                # Dashboard com altura fixa, não expande
                ft.Container(
                    content=self.dashboard.build(page),
                    #height=350,   # ⚡ altura fixa do dashboard
                    #clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    alignment=ft.alignment.center,
                    padding=ft.Padding(20, 0, 0, 0),
                    #expand=False
                ),

                # Categorias abaixo
                home_categories(),
            ],
            expand=True,                   # ⚡ importante: não expandir para tela inteira
            scroll=ft.ScrollMode.AUTO,      # permite scroll se necessário
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )'''

'''class HomeView:
    def __init__(self, conn):
        self.conn = conn
        self.dashboard = HomeDashboard(self.conn, GerenciarGraficos(conn))

    def _on_search(self, texto):
        print("Pesquisando por:", texto)

    def build(self, page: ft.Page):
        page.title = "Home"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[

                # ===== HEADER + DASHBOARD SOBREPOSTO =====
                ft.Stack(
                    clip_behavior=ft.ClipBehavior.NONE,
                    controls=[
                        # Header (fundo)
                        home_header(on_search=self._on_search),

                        #ft.Container(
                            #top=280,
                            #left=0,
                            #right=0,
                            #alignment=ft.alignment.center,
                            #content=self.dashboard.build(page),
                        #),
                        self.dashboard.build(page), 
                    ],
                ),

                # Espaço para compensar o dashboard flutuante
                #ft.Container(height=260),

                # ===== CATEGORIAS =====
                home_categories(),
            ],
        )'''

class HomeView:
    def __init__(self, conn):
        self.conn = conn
        self.dashboard = HomeDashboard(self.conn, GerenciarGraficos(conn))

    def build(self, page: ft.Page):
        page.title = "Home"
        page.padding = 0

        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # Header JÁ CONTÉM o dashboard
                home_header(dashboard=self.dashboard.build(page)),

                # Agora só o corpo rola
                home_categories(),
            ],
        )

