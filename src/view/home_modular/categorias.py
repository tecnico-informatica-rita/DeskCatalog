import flet as ft

def home_categories():
    def botao_de_categoria(text):
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
        )

    return ft.Column(
        controls=[
            ft.Row(
                [
                    botao_de_categoria("🏫 Salas / Laboratórios"),
                    botao_de_categoria("💻 Informática"),
                    botao_de_categoria("🎤 Áudio / Vídeo"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            ft.Row(
                [
                    botao_de_categoria("❄️ Infraestrutura"),
                    botao_de_categoria("🪑 Mobiliário"),
                    botao_de_categoria("🖋️ Material de Escritório"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            ft.Row(
                [
                    botao_de_categoria("🛡️ Segurança"),
                    botao_de_categoria("... Outros"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
