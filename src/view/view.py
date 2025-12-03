# view.py
"""
Camada View:
- Contém todas as funções responsáveis pela interação com o usuário.
- Funções de exibição e de obtenção de dados.
"""
import flet as ft
from src.database.database import separar_linhas_categoria_informatica

import flet as ft

def criar_card(produto, on_click_disponivel=None, on_click_indisponivel=None):
    nome = produto["Produto"]
    status = produto["Status"].lower()
    unidades = produto["Unidades"]

    if status == "disponível":
        cor_botao = ft.Colors.GREEN_400
        texto_botao = "Disponível"
        on_click = on_click_disponivel
    else:
        cor_botao = ft.Colors.RED_400
        texto_botao = "Indisponível"
        on_click = on_click_indisponivel

    return ft.Container(
        width=250,
        padding=15,
        border_radius=12,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(blur_radius=12, spread_radius=1, color="#00000020"),
        content=ft.Column([
            ft.Text(nome, weight=ft.FontWeight.BOLD, size=14),

            # BOTÃO DE STATUS
            ft.ElevatedButton(
                text=texto_botao,
                bgcolor=cor_botao,
                color=ft.Colors.WHITE,
                on_click=on_click
            ),

            ft.Text(f"Unidades: {unidades}"),
        ])
    )

def main(page: ft.Page):
    page.title = "Catálogo"
    page.scroll = "auto"
    cards = [criar_card(p) for p in separar_linhas_categoria_informatica]
    page.add(
        ft.Row(
            controls=cards,
            wrap=True,       
            spacing=20
        )
    )
ft.app(target=main)




