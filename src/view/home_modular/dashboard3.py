import flet as ft
import plotly.express as px
import pandas as pd
from flet.plotly_chart import PlotlyChart


class HomeDashboard:
    def __init__(self, dados_barra, dados_pizza, dados_empilhado):
        self.dados_barra = dados_barra
        self.dados_pizza = dados_pizza
        self.dados_empilhado = dados_empilhado

    # ---------------- GRÁFICO DE BARRAS ----------------
    def grafico_barra(self):
        df = pd.DataFrame(self.dados_barra)

        fig = px.bar(
            df,
            x="Categoria",
            y="Qtd",
            title="Empréstimos Diários por Categoria",
            color="Categoria",
            color_discrete_sequence=["#d2b0e9", "#e067c7", "#b551c7", "#00357a"],
        )

        return ft.Container(
            content=PlotlyChart(fig, expand=True),
            width=425,
            height=375,
        )

    # ---------------- GRÁFICO DE PIZZA ----------------
    def grafico_pizza(self):
        df = pd.DataFrame({
            "Item": list(self.dados_pizza.keys()),
            "Percentual": list(self.dados_pizza.values())
        })

        fig = px.pie(
            df,
            names="Item",
            values="Percentual",
            title="Ativos e Inativos",
            color_discrete_sequence=["#d2b0e9", "#e067c7", "#b551c7", "#00357a"],
        )

        return ft.Container(
            content=PlotlyChart(fig, expand=True),
            width=425,
            height=375,
        )

    # ---------------- GRÁFICO EMPILHADO ----------------
    def grafico_empilhado(self):
        df = pd.DataFrame(self.dados_empilhado)

        fig = px.bar(
            df,
            x="Categoria",
            y=[col for col in df.columns if col != "Categoria"],
            title="Itens Pendentes por Categoria",
            color_discrete_sequence=["#d2b0e9", "#e067c7", "#00357a"],
        )

        return ft.Container(
            content=PlotlyChart(fig, expand=True),
            width=425,
            height=375,
        )

    # ---------------- DASHBOARD FINAL ----------------
    def build(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.grafico_barra(),
                    self.grafico_pizza(),
                    self.grafico_empilhado(),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            margin=ft.Margin(top=330, left=0, right=0, bottom=0),
            alignment=ft.alignment.center,
        )
