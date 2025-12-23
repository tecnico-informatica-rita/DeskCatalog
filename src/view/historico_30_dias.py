import flet as ft
from src.controller.controller import mostrar_informaçoes_dos_ultimos_30_dias

class Relatorio30DiasView:
    def __init__(self):
        pass

    def main(self, page: ft.Page):
        page.title = "Relatório - Últimos 30 Dias"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT

        # ---(MENU LATERAL) PARA NAVEGAÇÃO ---
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

        
        dados = mostrar_informaçoes_dos_ultimos_30_dias()

        rows = []
        # CHECAGEM DE SEGURANÇA: Só tenta criar a tabela se 'dados' for uma lista de verdade
        if isinstance(dados, list):
            for item in dados:
                # Se o item for um dicionário, extraímos os dados com segurança
                if isinstance(item, dict):
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(item.get("Produto", "---")))),
                                ft.DataCell(ft.Text(str(item.get("Pessoa", "---")))),
                                ft.DataCell(ft.Text(str(item.get("Data_Emprestimo", "---")))), 
                                ft.DataCell(ft.Text(str(item.get("Quantidade", "0")))),
                                ft.DataCell(ft.Text(str(item.get("Status", "---"))))
                            ]
                        )
                    )
            
            conteudo_principal = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Produto", weight="bold")),
                    ft.DataColumn(ft.Text("Pessoa", weight="bold")),
                    ft.DataColumn(ft.Text("Data", weight="bold")),
                    ft.DataColumn(ft.Text("Qtd", weight="bold")),
                    ft.DataColumn(ft.Text("Status", weight="bold")),
                ],
                rows=rows 
            )
        else:
            
            mensagem_erro = str(dados) if dados else "Nenhum dado encontrado para o período."
            conteudo_principal = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.INFO_OUTLINE, color="amber", size=50),
                    ft.Text(mensagem_erro, size=18, color="amber", weight="bold", text_align="center")
                ], horizontal_alignment="center"),
                padding=50
            )

        # --- VIEW DA PÁGINA ---
        page.views.append(
            ft.View(
                route="/relatorios",
                drawer=drawer,
                appbar=ft.AppBar(
                    leading=ft.IconButton(ft.Icons.MENU, icon_color="white", on_click=lambda _: page.open(drawer)),
                    title=ft.Text("Relatório 30 Dias", color="white"),
                    bgcolor="#b551c7",
                    center_title=True
                ),
                controls=[
                    ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Container(
                                padding=ft.padding.all(30),
                                alignment=ft.alignment.center,
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            "Movimentações dos Últimos 30 Dias",
                                            size=28,
                                            weight=ft.FontWeight.BOLD,
                                            color="#b551c7",
                                            text_align="center"
                                        ),
                                        ft.Divider(height=30, color="transparent"),
                                        
                                        ft.Container(
                                            content=conteudo_principal,
                                            bgcolor="white",
                                            padding=20,
                                            border_radius=15,
                                            shadow=ft.BoxShadow(blur_radius=15, color="#00000015"),
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ]
            )
        )
        page.update()