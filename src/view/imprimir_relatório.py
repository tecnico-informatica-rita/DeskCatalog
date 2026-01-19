import flet as ft
from controller.controller import mostrar_informaçoes_dos_ultimos_30_dias

class Relatorio30DiasView:
    def __init__(self, conn):
        self.conn = conn
        
    def main(self, page: ft.Page):
        page.title = "Relatório de emprestimos não devolvidos - Últimos 30 Dias"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.resizable = True

        #Ajuda ------------------------------------------------------------------------------------------------------------
        def fechar_snack():
            snack_bar.open = False
            page.update()
 
        snack_bar = ft.SnackBar(
            content=ft.Text("Aqui você vê os empréstimos dos últimos 30 dias. Use o menu para novas ações."),
            action="OK",
            on_action=lambda _: fechar_snack(),
            duration=9000,
        )
        page.overlay.append(snack_bar)
 
        def abrir_ajuda(e):
            snack_bar.open = True
            page.update()
 
        #Início Menu ---------------------------------------------------------------------------------------------------------------
        page.drawer = ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination("Relatório", icon=ft.Icons.DOWNLOAD),
                ft.NavigationDrawerDestination("Cadastrar Item", icon=ft.Icons.ADD_CIRCLE),
                ft.NavigationDrawerDestination("Empréstimo", icon=ft.Icons.WIDGETS),
                ft.NavigationDrawerDestination("Devolução", icon=ft.Icons.REPLAY),
                ft.NavigationDrawerDestination("Início", icon=ft.Icons.HOME)
            ]
        )
 
        #Barra de Menu ------------------------------------------------------------------------------------------------------------
        page.appbar = ft.AppBar(
            leading=ft.Container(
                width=50,
                height=50,
                bgcolor="#b551c7",
                border_radius=50,
                content=ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.MENU,
                            icon_size=30,
                            icon_color="white",
                            on_click=lambda _: page.open(page.drawer),
                        )
                    ],
                    alignment="center",
                    vertical_alignment="center",
                ),
            ),
            title=ft.Text("", size=22, color=ft.Colors.WHITE),
            bgcolor="#b551c7",
            actions=[
                ft.Container(
                    width=40,
                    height=40,
                    bgcolor="white",
                    border_radius=50,
                    ink=True,
                    margin=ft.Margin(0, 0, 20, 0),
                    on_click=abrir_ajuda,
                    content=ft.Icon(
                        ft.Icons.QUESTION_MARK,
                        color="#b551c7",
                        size=30,
                    ),
                )
            ],
        )

        dados = mostrar_informaçoes_dos_ultimos_30_dias(self.conn)

        if isinstance(dados, str):
            page.add(ft.Text(dados, color="red"))
            return

        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["Produto"])),
                    ft.DataCell(ft.Text(item["Pessoa"])),
                    ft.DataCell(ft.Text(item["Data_Emprestimo"])),
                    ft.DataCell(ft.Text(str(item["Quantidade"]))),
                    ft.DataCell(ft.Text(item["Status"])),
                ]
            )
            for item in dados
        ]

        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Produto")),
                ft.DataColumn(ft.Text("Pessoa")),
                ft.DataColumn(ft.Text("Data Empréstimo")),
                ft.DataColumn(ft.Text("Quantidade")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=rows
        )

        layout_principal = ft.Container(
            expand=True,
            bgcolor="#ffffff",
            padding=0,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment="center",
                spacing=25,
                controls=[
                    ft.Container(
                        expand=True,
                        height=250,
                        image=ft.DecorationImage(
                            src="img/historico.gif",
                            fit=ft.ImageFit.COVER,
                        ),
                    ),
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
                                    color="#cccccc",
                                ),
                                content=ft.Column(
                                    expand=True,
                                    spacing=25,
                                    horizontal_alignment="center",
                                    controls=[
                                        ft.Divider(),
                                        ft.Text("📋 Relatório de 30 dias", size=22),
                                        tabela,
                                    ]
                                ),
                            )
                        ]
                    ),
                ]
            )
        )

        return layout_principal
#Deve ser puxado pelo arquivo main
'''
def main(page: ft.Page):
    view = Relatorio30DiasView()
    view.main(page)

ft.app(target=main)
'''