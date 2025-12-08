import flet as ft
from src.controller.controller import autenticar_loguin_completo
from src.database.database import popular_dados_login


def main(page: ft.Page):
    page.title = "Login + Fase de teste + Lista"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    email = ft.TextField(label="Email", width=300)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)

    lista_usuario = []

    def login(e):
        nonlocal lista_usuario

        resultado = autenticar_loguin_completo(email.value, senha.value)
        print("Resultado autenticação:", resultado)

        if resultado:
            lista_usuario = [(email.value, senha.value)]  

          
            salvou, mensagem = popular_dados_login(lista_usuario)

            if not salvou:
                page.snack_bar = ft.SnackBar(ft.Text(mensagem))
                page.snack_bar.open = True
                page.update()
                return
            
            mostrar_fase_teste()

        else:
            page.snack_bar = ft.SnackBar(ft.Text("Email inválido ou senha fraca!"))
            page.snack_bar.open = True
            page.update()

    def mostrar_fase_teste():
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    ft.Text(" FASE DE TESTE ", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("O botão de login funcionouuu"),
                    ft.ElevatedButton("Voltar ao login", on_click=voltar_login)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def voltar_login(e):
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
                    email,
                    senha,
                    btn_login
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    btn_login = ft.ElevatedButton("Entrar", on_click=login)

    page.add(
        ft.Column(
            [
                ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
                email,
                senha,
                btn_login
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


ft.app(target=main, view=ft.WEB_BROWSER)
