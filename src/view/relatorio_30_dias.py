import flet as ft
from src.controller.controller import mostrar_informaçoes_dos_ultimos_30_dias

class Relatorio30DiasView:
    
    def main(self, page: ft.Page):
        page.title = "Relatório de emprestimos não devolvidos - Últimos 30 Dias"
        page.padding = 20
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.resizable = True

        dados = mostrar_informaçoes_dos_ultimos_30_dias()

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

        page.add(
            ft.Column(
                [
                    ft.Text("Relatório dos Últimos 30 Dias",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color="#b551c7"),
                    tabela
                ],
                scroll=ft.ScrollMode.AUTO
            )
        )