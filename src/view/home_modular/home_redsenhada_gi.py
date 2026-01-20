import flet as ft

from view.home_modular.header import home_header
from view.home_modular.categorias import home_categories
from view.home_modular.dashboard2 import HomeDashboard
from model.model_deskcatalog import GerenciarGraficos


class HomeView:
    def __init__(self, conn):
        self.conn = conn
        self.model = GerenciarGraficos(conn)

    def build_layout(self, page: ft.Page):
        # 🔹 Dados vindos do model (ou mock por enquanto)
        dados_barra = self.model.grafico_empCatDiarios()
        dados_pizza = self.model.grafico_comparacao_ativos_inativos()
        dados_pendentes = self.model.grafico_itens_pendentesCat()

        graficos = HomeDashboard(
            dados_barra=dados_barra,
            dados_pizza=dados_pizza,
            dados_empilhado=dados_pendentes,
        )

        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # Header recebe os gráficos
                home_header(
                    dashboard=graficos.build()
                ),

                # Categorias abaixo
                home_categories(page),
            ],
        )

    def main_home(self, page: ft.Page):
        page.title = "Home"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT

        # 🔹 Navegação
        from view.home_modular.navegacao import criar_navigation
        appbar, drawer = criar_navigation(page)
        page.appbar = appbar
        page.drawer = drawer

        # 🔹 Retorna o layout (NÃO usar page.add aqui)
        return self.build_layout(page)
