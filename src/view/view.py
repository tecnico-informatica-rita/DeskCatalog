# view.py
"""
Camada View:
- Contém todas as funções responsáveis pela interação com o usuário.
- Funções de exibição e de obtenção de dados.
"""
import flet as ft
from src.database.database import a

def criar_card(produto):
    nome = produto["Produto"]
    status = produto["Status"]
    unidades = produto["Unidades"]

    cor_status = ft.Colors.GREEN_400 if status.lower() == "disponível" else ft.Colors.RED_400

    return ft.Container(
        width=250,
        padding=15,
        border_radius=12,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(blur_radius=12, spread_radius=1, color="#00000020"),
        content=ft.Column([
            ft.Text(nome, weight=ft.FontWeight.BOLD, size=14),
            ft.Text(f"Status: {status}", color=cor_status),
            ft.Text(f"Unidades: {unidades}")
        ])
    )

def main(page: ft.Page):
    page.title = "Catálogo"
    page.scroll = "auto"

    # cria todos os cards
    cards = [criar_card(p) for p in a]

    # adiciona na tela
    page.add(
        ft.Row(
            controls=cards,
            wrap=True,       
            spacing=20
        )
    )

ft.app(target=main)




