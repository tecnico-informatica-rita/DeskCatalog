import flet as ft
from src.model.model import separar_o_retorno_por_variavel, pegar_linhas_da_view_do_banco
linhas = pegar_linhas_da_view_do_banco('visao_informatica')
informatica = separar_o_retorno_por_variavel(linhas)
print(informatica)

def criar_card(produto, on_click_disponivel=None, on_click_indisponivel=None):
    nome = produto["Produto"]
    status = produto["Status"]
    unidades = produto["Unidades"]

    if status == "Ativo":
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

            #STATUS
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
    page.title = "INFORMÁTICA"
    page.scroll = "auto"
    cards = [criar_card(p) for p in informatica]
    page.add(
        ft.Row(
            controls=cards,
            wrap=True,       
            spacing=20
        )
    )
ft.app(target=main)