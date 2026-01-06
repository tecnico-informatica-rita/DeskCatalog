import flet as ft
from src.controller.controller import autenticar_loguin_completo
from src.database.database import popular_dados_login

def main(page: ft.Page):
    page.title = "Login"
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    email = ft.TextField(label="Email", width=300)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)

    lista_usuario = []

    def criar_layout():
        return ft.Container(
            expand=True,
            bgcolor="#ffffff",
            padding=0,
            content=ft.Column(
                [
                    ft.Stack(
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        width=800,
                                        bgcolor="white",
                                        border_radius=40,
                                        padding=40,
                                        shadow=ft.BoxShadow(
                                            blur_radius=20,
                                            spread_radius=5,
                                            color="#ffffff",
                                        ),
                                        content=ft.Container(
                                            padding=75,
                                            content=ft.Column(
                                                alignment=ft.alignment.top_center,
                                                expand=True,
                                                spacing=25,
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("Login",size=30, color="#b551c7"),
                                                    email,
                                                    senha,
                                                    ft.Container(
                                                        alignment=ft.alignment.center,
                                                        content=ft.ElevatedButton(
                                                            "Entrar",
                                                            color=ft.Colors.WHITE,
                                                            bgcolor="#b551c7",
                                                            height=50,
                                                            width=300,
                                                            on_click=login,
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ft.Row([], alignment=ft.MainAxisAlignment.CENTER),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
        )

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
                    ft.Text("O botão de login funcionou caralhoooooooooo"),
                    ft.ElevatedButton("Voltar ao login", on_click=voltar_login)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def voltar_login(e):
        page.controls.clear()
        page.add(criar_layout())
        page.update()
    
    page.add(criar_layout())

ft.app(target=main, view=ft.WEB_BROWSER)
