import flet as ft
from src.controller.controller import mostrar_historico_transacoes_de_emprestimo

class HistoricoView:
    def main(self, page: ft.Page):
        page.title = "Histórico de Empréstimos"
        page.padding = 20
        page.bgcolor = "#ffffff"

       
        dados =  mostrar_historico_transacoes_de_emprestimo()

        colunas = [
            ft.DataColumn(ft.Text("Produto")),
            ft.DataColumn(ft.Text("Emprestado por")),
            ft.DataColumn(ft.Text("Data do Empréstimo")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Quantidade")),
        ]

        # Cria as linhas
        linhas = []
        for item in dados:
            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["Produto"])),
                        ft.DataCell(ft.Text(item["Emprestado_por"])),
                        ft.DataCell(ft.Text(item["Data_emprestimo"])),
                        ft.DataCell(ft.Text(item["Status"])),
                        ft.DataCell(ft.Text(str(item["Quantidade_total"]))),
                    ]
                )
            )

        # Tabelinhaaaaaa
        tabela = ft.DataTable(
            columns=colunas,
            rows=linhas,
            data_text_style=ft.TextStyle(size=14),
            heading_row_color=ft.Colors.GREY_200,
            horizontal_lines=ft.BorderSide(1, "#DDDDDD"),
            vertical_lines=ft.BorderSide(1, "#DDDDDD")
        )


        page.add(
            ft.Column(
                [
                    ft.Text(
                        "Histórico de Empréstimos",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#b551c7"
                    ),
                    ft.Container(
                        content=tabela,
                        expand=True,
                        padding=10,
                    )
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            )
        )
def main(page: ft.Page):
    HistoricoView().main(page)

if __name__ == "__main__":
    import flet as ft
    ft.app(target=main)
