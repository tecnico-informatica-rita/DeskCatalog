import flet as ft

def home_categories(page: ft.Page):
    def botao_de_categoria(text, rota):
        return ft.ElevatedButton(
            content=ft.Text(
                text,
                size=22,
                color=ft.Colors.WHITE,
                weight="w500",
            ),
            bgcolor="#b551c7",
            width=350,
            height=100,
            on_click=lambda _: page.go(rota)
        )

    return ft.Column(
        controls=[
            ft.Row(
                [
                    botao_de_categoria("🏫 Salas / Laboratórios", "/sala"),
                    botao_de_categoria("💻 Informática", "/informatica"),
                    botao_de_categoria("🎤 Áudio / Vídeo", "/audio"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            ft.Row(
                [
                    botao_de_categoria("❄️ Infraestrutura", "/infraestrutura"),
                    botao_de_categoria("🪑 Mobiliário", "/mobiliario"),
                    botao_de_categoria("🖋️ Material de Escritório", "/material"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            ft.Row(
                [
                    botao_de_categoria("🛡️ Segurança", "/seguranca"),
                    botao_de_categoria("... Outros", "/outros"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
