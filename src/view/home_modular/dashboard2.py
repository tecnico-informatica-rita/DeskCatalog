'''import flet as ft
import asyncio

class HomeDashboard:
    def __init__(self, conn, model):
        self.conn = conn
        self.model = model

        self.coluna = ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ===============================
    # BUILD
    # ===============================
    def build(self, page: ft.Page):
        self.page = page
        page.run_task(self._carregar_dados)

        return ft.Container(
            padding=30,
            content=self.coluna,
        )

    # ===============================
    # CARREGA / ATUALIZA
    # ===============================
    async def _carregar_dados(self):
        await asyncio.sleep(0.1)
        self.refresh()

    def refresh(self):
        self.coluna.controls.clear()

        self.coluna.controls.extend([
            self._grafico_barras(
                "Empréstimos por Categoria",
                self.model.grafico_empCatDiarios()
            ),
            self._grafico_pizza_fake(
                "Ativos x Inativos",
                self.model.grafico_comparacao_ativos_inativos()
            ),
            self._grafico_barras(
                "Itens Pendentes",
                self.model.grafico_itens_pendentesCat()
            ),
        ])

        self.page.update()

    # ===============================
    # GRÁFICOS
    # ===============================
    def _grafico_barras(self, titulo, dados):
        if not dados:
            return ft.Text("Sem dados")

        total = max(item["Qtd"] for item in dados)

        barras = []
        for item in dados:
            barras.append(
                ft.Column(
                    [
                        ft.Text(item["Categoria"], size=12),
                        ft.Container(
                            width=300 * (item["Qtd"] / total),
                            height=20,
                            bgcolor="#b551c7",
                            border_radius=10,
                        ),
                        ft.Text(str(item["Qtd"]), size=11),
                    ],
                    spacing=5,
                )
            )

        return self._card(titulo, barras)

    def _grafico_pizza_fake(self, titulo, dados):
        total = sum(dados.values())
        linhas = []

        for k, v in dados.items():
            linhas.append(
                ft.Row(
                    [
                        ft.Container(
                            width=15,
                            height=15,
                            bgcolor="#b551c7",
                            border_radius=5,
                        ),
                        ft.Text(f"{k}: {v} ({int((v/total)*100)}%)"),
                    ],
                    spacing=10,
                )
            )

        return self._card(titulo, linhas)

    # ===============================
    # CARD PADRÃO
    # ===============================
    def _card(self, titulo, conteudo):
        return ft.Container(
            width=420,
            padding=20,
            bgcolor="white",
            border_radius=15,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.15, "black"),
            ),
            content=ft.Column(
                [
                    ft.Text(titulo, size=16, weight="bold"),
                    ft.Divider(),
                    *conteudo,
                ],
                spacing=10,
            ),
        ) # graficos no lugar errado''' 

import flet as ft


class HomeDashboard:
    def __init__(self, conn, model):
        self.conn = conn
        self.model = model

    def build(self, page: ft.Page):
        dados_barra = self.model.grafico_empCatDiarios()
        dados_pizza = self.model.grafico_comparacao_ativos_inativos()
        dados_pendentes = self.model.grafico_itens_pendentesCat()

        return ft.Row(
            spacing=30,
            wrap=True,  # quebra linha se faltar espaço
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self._grafico_barra(
                    "Empréstimos por Categoria",
                    dados_barra,
                    "Categoria",
                    "Qtd",
                ),
                self._grafico_pizza(
                    "Ativos x Inativos",
                    dados_pizza,
                ),
                self._grafico_barra(
                    "Itens Pendentes",
                    dados_pendentes,
                    "Categoria",
                    "Qtd",
                ),
            ],
        )

    # ======================
    # GRÁFICO DE BARRA
    # ======================
    def _grafico_barra(self, titulo, dados, label_key, value_key):
        max_valor = max(item[value_key] for item in dados) or 1

        linhas = []
        for item in dados:
            linhas.append(
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(item[label_key], size=13),
                        ft.ProgressBar(
                            value=item[value_key] / max_valor,
                            height=6,
                            color="#b455c6",
                            bgcolor="#eadcf1",
                        ),
                        ft.Text(
                            str(item[value_key]),
                            size=12,
                            color=ft.Colors.GREY,
                        ),
                    ],
                )
            )

        return self._card(titulo, linhas)

    # ======================
    # "PIZZA" SIMULADO
    # ======================
    def _grafico_pizza(self, titulo, dados):
        total = sum(dados.values()) or 1

        linhas = []
        for label, valor in dados.items():
            linhas.append(
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            width=12,
                            height=12,
                            border_radius=6,
                            bgcolor="#b455c6",
                        ),
                        ft.Text(
                            f"{label}: {valor} ({int(valor / total * 100)}%)"
                        ),
                    ],
                )
            )

        return self._card(titulo, linhas)

    # ======================
    # CARD DO GRÁFICO
    # ======================
    def _card(self, titulo, conteudo):
        return ft.Container(
            width=360,
            padding=20,
            border_radius=20,
            bgcolor=ft.Colors.WHITE,  # cartão individual
            shadow=ft.BoxShadow(
                blur_radius=18,
                color=ft.Colors.with_opacity(0.08, "black"),
            ),
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD),
                    *conteudo,
                ],
            ),
        )
