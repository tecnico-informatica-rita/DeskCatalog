import flet as ft
from src.view.home import main as home_main
from src.controller.controller import autenticar_loguin_completo
from src.database.database import popular_dados_login

def main(page: ft.Page):
    page.title = "Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email = ft.TextField(label="Email", width=300)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)

    def login(e):
        usuario = email.value
        senha_usuario = senha.value

       
        if autenticar_loguin_completo(usuario, senha_usuario):
            
            salvou, msg = popular_dados_login([(usuario, senha_usuario)])
            if not salvou:
                page.snack_bar = ft.SnackBar(ft.Text(msg))
                page.snack_bar.open = True
                page.update()
                return
            
            
            page.controls.clear()
            home_main(page)  
            page.update()

        else:
            page.snack_bar = ft.SnackBar(ft.Text("Email inválido ou senha incorreta."))
            page.snack_bar.open = True
            page.update()

    btn_login = ft.ElevatedButton("Entrar", on_click=login)

    
    page.add(
        ft.Column(
            [
                ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
                email,
                senha,
                btn_login,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
