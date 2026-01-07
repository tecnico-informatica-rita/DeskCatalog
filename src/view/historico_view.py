import flet as ft
from controller.controller import mostrar_historico_transacoes_de_emprestimo

class HistoricoView:
    def __init__(self, conn):
        self.conn = conn

    def main(self, page: ft.Page):
        page.title = "Histórico de Empréstimos"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT

        # (MENU LATERAL) ---
        drawer = ft.NavigationDrawer(
            on_change=lambda e: page.go([
                "/audio", "/sala", "/informatica", "/infraestrutura", 
                "/mobiliario", "/material", "/seguranca", "/outros", 
                "/", "/relatorios", "/historico"
            ][e.control.selected_index]),
            controls=[
                ft.NavigationDrawerDestination(label="Áudio / Vídeo", icon=ft.Icons.VIDEO_CAMERA_FRONT),
                ft.NavigationDrawerDestination(label="Sala / Laboratório", icon=ft.Icons.BIOTECH),
                ft.NavigationDrawerDestination(label="Informática", icon=ft.Icons.LAPTOP),
                ft.NavigationDrawerDestination(label="Infraestrutura", icon=ft.Icons.CABLE),
                ft.NavigationDrawerDestination(label="Mobiliário", icon=ft.Icons.WEEKEND),
                ft.NavigationDrawerDestination(label="Material de Escritório", icon=ft.Icons.EDIT),
                ft.NavigationDrawerDestination(label="Segurança", icon=ft.Icons.SECURITY),
                ft.NavigationDrawerDestination(label="Outros", icon=ft.Icons.MISCELLANEOUS_SERVICES),
                ft.Divider(),
                ft.NavigationDrawerDestination(label="Início", icon=ft.Icons.HOME),
                ft.NavigationDrawerDestination(label="Relatórios", icon=ft.Icons.ASSESSMENT),
                ft.NavigationDrawerDestination(label="Histórico", icon=ft.Icons.HISTORY),
            ]
        )

        # --- BUSCA OS DADOS ---
        dados = mostrar_historico_transacoes_de_emprestimo(self.conn)

        linhas = []
        
        
        if isinstance(dados, list):
            for item in dados:
                if isinstance(item, dict):
                    linhas.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(item.get("Produto", "---")))),
                                ft.DataCell(ft.Text(str(item.get("Emprestado_por", "---")))),
                                ft.DataCell(ft.Text(str(item.get("Data_emprestimo", "---")))),
                                ft.DataCell(ft.Text(str(item.get("Status", "---")))),
                                ft.DataCell(ft.Text(str(item.get("Quantidade_total", "0")))),
                            ]
                        )
                    )
            
            conteudo_body = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Produto")),
                    ft.DataColumn(ft.Text("Emprestado por")),
                    ft.DataColumn(ft.Text("Data")),
                    ft.DataColumn(ft.Text("Status")),
                    ft.DataColumn(ft.Text("Qtd")),
                ],
                rows=linhas,
                heading_row_color=ft.Colors.GREY_100,
            )
        else:
            
            mensagem = str(dados) if dados else "Nenhum histórico disponível."
            conteudo_body = ft.Container(
                content=ft.Text(mensagem, color="red", weight="bold"),
                padding=20
            )

        
        page.views.append(
            ft.View(
                route="/historico",
                drawer=drawer,
                appbar=ft.AppBar(
                    leading=ft.IconButton(ft.Icons.MENU, icon_color="white", on_click=lambda _: page.open(drawer)),
                    title=ft.Text("Histórico", color="white"),
                    bgcolor="#b551c7"
                ),
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                padding=30,
                                content=ft.Column([
                                    ft.Text("Histórico de Empréstimos", size=28, weight="bold", color="#b551c7"),
                                    ft.Container(
                                        content=conteudo_body,
                                        bgcolor="white",
                                        padding=15,
                                        border_radius=10,
                                        shadow=ft.BoxShadow(blur_radius=10, color="#00000015")
                                    )
                                ], horizontal_alignment="center")
                            )
                        ]
                    )
                ]
            )
        )
        page.update()
