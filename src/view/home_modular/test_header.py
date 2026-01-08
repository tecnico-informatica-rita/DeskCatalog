import flet as ft
from header import home_header


'''def main(page: ft.Page):
    page.title = "Teste Header"
    page.padding = 0
    page.scroll = "auto"

    page.add(home_header())


ft.app(target=main, assets_dir="../../assets")'''

'''import flet as ft
from categorias import home_categories

def main(page: ft.Page):
    page.add(home_categories())

ft.app(target=main)'''

'''import flet as ft
from home_redesenhada import HomeView

def main(page: ft.Page):
    home = HomeView(conn=None)  # sem banco por enquanto
    page.add(home.build(page))

ft.app(target=main, assets_dir="../../assets")'''


from navegacao import criar_navigation

def main(page: ft.Page):
    appbar, drawer = criar_navigation(page)

    page.appbar = appbar
    page.drawer = drawer

    page.add(
        ft.Text(
            "Teste da Navigation",
            size=30,
            weight="bold"
        )
    )

ft.app(target=main)
import flet as ft

'''# ===== MODEL FAKE SÓ PARA TESTE =====
class FakeGerenciarGraficos:
    def grafico_empCatDiarios(self):
        return [
            {"Categoria": "Eletrônicos", "Qtd": 15},
            {"Categoria": "Móveis", "Qtd": 5},
            {"Categoria": "Periféricos", "Qtd": 20},
        ]

    def grafico_comparacao_ativos_inativos(self):
        return {"Ativos": 10, "Inativos": 3}

    def grafico_itens_pendentesCat(self):
        return [
            {"Categoria": "Livros", "Qtd": 8},
            {"Categoria": "Ferramentas", "Qtd": 3},
        ]


# ===== IMPORTA SEU DASHBOARD =====
from dashboard import HomeDashboard


def main(page: ft.Page):
    page.title = "Teste Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 1300
    page.window_height = 800

    # Cria dashboard SEM banco
    dashboard = HomeDashboard(conn=None, model= FakeGerenciarGraficos())

    
    page.add(dashboard.build(page))


if __name__ == "__main__":
    ft.app(target=main)'''
