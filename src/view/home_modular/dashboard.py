'''import flet as ft
import pandas as pd
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import asyncio

class HomeDashboard:
    def __init__(self, conn, model):
        self.conn = conn
        self.model = model

        # Container dos gráficos
        self.container_graficos = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            wrap=True,
            visible=False,
            animate_opacity=300,
            expand=False
        )

        # Loading
        self.loading = ft.Column(
            [
                ft.ProgressRing(width=50, height=50, stroke_width=4, color="#b551c7"),
                ft.Text(
                    "Carregando gráficos...",
                    color="#b551c7",
                    size=16,
                    weight="w500",
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            visible=True,
            expand=False
        )

    def build(self, page: ft.Page):
        """
        Retorna o container do dashboard
        """
        page.run_task(self._carregar_graficos)

        return ft.Container(
            padding=40,
            height=350,
            margin=ft.Margin(20, 0, 0, 0),
            content=ft.Column(
                [
                    self.loading,
                    self.container_graficos,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=False
            ),
        )

    async def _carregar_graficos(self):
        """
        Busca dados no model e monta os gráficos
        """
        await asyncio.sleep(0.6)  # efeito visual suave

        try:
            # ===== GRÁFICO 1: Empréstimos por categoria =====
            dados_barra = self.model.grafico_empCatDiarios()
            df_barra = pd.DataFrame(dados_barra)

            fig_barra = px.bar(
                df_barra,
                x="Categoria",
                y="Qtd",
                title="Empréstimos por Categoria",
                color="Categoria",
                color_discrete_sequence=["#d2b0e9", "#e067c7", "#b551c7"],
            )

            # ===== GRÁFICO 2: Ativos x Inativos =====
            dados_pizza = self.model.grafico_comparacao_ativos_inativos()
            df_pizza = pd.DataFrame(
                {
                    "Status": dados_pizza.keys(),
                    "Qtd": dados_pizza.values(),
                }
            )

            fig_pizza = px.pie(
                df_pizza,
                names="Status",
                values="Qtd",
                title="Ativos e Inativos",
                color_discrete_sequence=["#d2b0e9", "#b551c7"],
            )

            # ===== GRÁFICO 3: Itens pendentes =====
            dados_pendentes = self.model.grafico_itens_pendentesCat()
            df_pendentes = pd.DataFrame(dados_pendentes)

            fig_pendentes = px.bar(
                df_pendentes,
                x="Categoria",
                y="Qtd",
                title="Itens Pendentes por Categoria",
                color_discrete_sequence=["#d2b0e9"],
            )

            # ===== Ajustes visuais padrão =====
            for fig in [fig_barra, fig_pizza, fig_pendentes]:
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=320,
                    margin=dict(l=10, r=10, t=50, b=10),
                )

            # Limpa e adiciona gráficos
            self.container_graficos.controls.clear()

            for fig in [fig_barra, fig_pizza, fig_pendentes]:
                container = ft.Container(
                        content=PlotlyChart(fig, expand=False),
                        width=380,
                        height=320,
                        bgcolor="white",
                        border_radius=15,
                        padding=10,
                        shadow=ft.BoxShadow(
                            blur_radius=15,
                            color=ft.Colors.with_opacity(0.1, "black"),
                        ),
                    )
                container.mouse_events = False
                self.container_graficos.controls.append(container)

            # Exibe gráficos
            self.loading.visible = False
            self.container_graficos.visible = True

        except Exception as e:
            self.loading.controls.append(
                ft.Text(f"Erro ao carregar gráficos: {e}", color="red")
            )

        finally:
            self.loading.page.update()'''

import flet as ft
import pandas as pd
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import asyncio

class HomeDashboard:
    def __init__(self, conn, model):
        self.conn = conn
        self.model = model

        # Container dos gráficos
        self.container_graficos = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            wrap=True,
            visible=False,  # inicialmente escondido até os gráficos carregarem
            expand=False,
            vertical_alignment=ft.CrossAxisAlignment.START    # ⚡ não ocupa toda a tela
        )

        # Loading
        self.loading = ft.Column(
            [
                ft.ProgressRing(width=50, height=50, stroke_width=4, color="#b551c7"),
                ft.Text(
                    "Carregando gráficos...",
                    color="#b551c7",
                    size=16,
                    weight="w500",
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            visible=True,
            expand=False
        )

    def build(self, page: ft.Page):
        """
        Retorna o container do dashboard
        """
        self.page = page  # ⚡ salva referência do page para atualizações
        page.run_task(self._carregar_graficos)

        # ⚡ Container principal do dashboard
        return ft.Container(
            padding=20,
            height=350,  # altura fixa para não sobrepor o AppBar
            content=ft.Column(
                [
                    self.loading,
                    self.container_graficos,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=False
            ),
        )

    async def _carregar_graficos(self):
        """
        Carrega os gráficos de forma assíncrona
        """
        await asyncio.sleep(0.6)  # efeito visual suave

        try:
            # ===== GRÁFICO 1 =====
            dados_barra = self.model.grafico_empCatDiarios()
            df_barra = pd.DataFrame(dados_barra)
            fig_barra = px.bar(
                df_barra,
                x="Categoria",
                y="Qtd",
                title="Empréstimos por Categoria",
                color="Categoria",
                color_discrete_sequence=["#d2b0e9", "#e067c7", "#b551c7"],
            )

            # ===== GRÁFICO 2 =====
            dados_pizza = self.model.grafico_comparacao_ativos_inativos()
            df_pizza = pd.DataFrame({
                "Status": dados_pizza.keys(),
                "Qtd": dados_pizza.values()
            })
            fig_pizza = px.pie(
                df_pizza,
                names="Status",
                values="Qtd",
                title="Ativos e Inativos",
                color_discrete_sequence=["#d2b0e9", "#b551c7"],
            )

            # ===== GRÁFICO 3 =====
            dados_pendentes = self.model.grafico_itens_pendentesCat()
            df_pendentes = pd.DataFrame(dados_pendentes)
            fig_pendentes = px.bar(
                df_pendentes,
                x="Categoria",
                y="Qtd",
                title="Itens Pendentes por Categoria",
                color_discrete_sequence=["#d2b0e9"],
            )

            # ===== Ajustes visuais =====
            for fig in [fig_barra, fig_pizza, fig_pendentes]:
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=320,
                    margin=dict(l=10, r=10, t=50, b=10),
                )

            # Limpa e adiciona gráficos
            '''self.container_graficos.controls.clear()
            for fig in [fig_barra, fig_pizza, fig_pendentes]:
                grafico_container = ft.Container(
                    content=PlotlyChart(fig, expand=False),  # ⚡ expand=False
                    width=380,
                    height=320,
                    bgcolor="white",
                    border_radius=15,
                    padding=10,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    shadow=ft.BoxShadow(
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.1, "black"),
                    ),
                )
                self.container_graficos.controls.append(grafico_container)'''
            
            self.container_graficos.controls.clear()
            for fig in [fig_barra, fig_pizza, fig_pendentes]:
                grafico_container = ft.Container(
                # ⚡ ADICIONAMOS UM GESTURE DETECTOR PARA CONTROLAR O FOCO
                content=ft.IgnorePointer(
                    active=False, 
                    content=PlotlyChart(fig, expand=False)
                ),
                width=380,
                height=320,
                bgcolor="white",
                border_radius=15,
                padding=10,
                
                # ⚡ ESSA LINHA ABAIXO É O SEGREDO
                clip_behavior=ft.ClipBehavior.HARD_EDGE, 
                shadow=ft.BoxShadow(
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.1, "black"),
                ),
            )
            self.container_graficos.controls.append(grafico_container)

            # Exibe os gráficos e esconde o loading
            self.loading.visible = False
            self.container_graficos.visible = True

        except Exception as e:
            self.loading.controls.append(
                ft.Text(f"Erro ao carregar gráficos: {e}", color="red")
            )

        finally:
            # ⚡ Atualiza a página usando a referência do page salva
            self.page.update()
