import flet as ft
from mock_controller import MockController
from cadastro import pagina_produtos
from emprestimo import pagina_emprestimo

def main(page: ft.Page):
    page.title = "Sistema DeskCatalog"
    controller = MockController()
    conteudo = ft.Column()
    page.add(conteudo)

    # Funções de navegação
    def mostrar_produtos(e):
        conteudo.controls.clear()
        layout = pagina_produtos(controller, page)
        conteudo.controls.append(layout)
        page.update()

    def mostrar_emprestimos(e):
        conteudo.controls.clear()
        layout = pagina_emprestimo(controller, page)
        conteudo.controls.append(layout)
        page.update()

    menu = ft.Row([
        ft.ElevatedButton("Catálogo de Produtos", on_click=mostrar_produtos),
        ft.ElevatedButton("Empréstimos", on_click=mostrar_emprestimos)
    ])

    page.add(menu)
    mostrar_produtos(None)

ft.app(target=main)