import plotly.express as px
import flet as ft
from flet.plotly_chart import PlotlyChart
import pandas as pd
import asyncio

class home_view_arquivo:
    def __init__(self, conn):
        self.conn = conn
        self.container_graficos = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            wrap=True,
            visible=False,
            animate_opacity=300
        )

        self.loading_indicator = ft.Column(
            [
                ft.ProgressRing(width=50, height=50, stroke_width=4, color="#b551c7"),
                ft.Text("Carregando gráficos...", color="#b551c7", size=16, weight="w500")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            visible=True
        )

    def main_home_arquivo(self, page: ft.Page):
        page.title = "Home"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        # --- FUNÇÕES DE APOIO ---
        def fechar_app(e):
            import os
            os._exit(0)

        # --- MENU LATERAL 
        drawer = ft.NavigationDrawer(
            on_change=lambda e: page.go([
                "/audio",           # 0
                "/sala",            # 1
                "/informatica",     # 2
                "/infraestrutura",  # 3
                "/mobiliario",      # 4
                "/material",        # 5
                "/seguranca",       # 6
                "/outros",          # 7
                "/",                # 8 (Início)
                "/relatorios",      # 9
                "/historico"        # 10
            ][e.control.selected_index]),
            controls=[
                ft.NavigationDrawerDestination(label="Áudio / Vídeo", icon=ft.Icons.VIDEO_CAMERA_FRONT), # 0
                ft.NavigationDrawerDestination(label="Sala / Laboratório", icon=ft.Icons.BIOTECH),         # 1
                ft.NavigationDrawerDestination(label="Informática", icon=ft.Icons.LAPTOP),              # 2
                ft.NavigationDrawerDestination(label="Infraestrutura", icon=ft.Icons.CABLE),            # 3
                ft.NavigationDrawerDestination(label="Mobiliário", icon=ft.Icons.WEEKEND),              # 4
                ft.NavigationDrawerDestination(label="Material de Escritório", icon=ft.Icons.EDIT),     # 5
                ft.NavigationDrawerDestination(label="Segurança", icon=ft.Icons.SECURITY),              # 6
                ft.NavigationDrawerDestination(label="Outros", icon=ft.Icons.MISCELLANEOUS_SERVICES),    # 7
                ft.Divider(),
                ft.NavigationDrawerDestination(label="Início", icon=ft.Icons.HOME),                    # 8
                ft.NavigationDrawerDestination(label="Relatórios", icon=ft.Icons.ASSESSMENT),          # 9
                ft.NavigationDrawerDestination(label="Histórico", icon=ft.Icons.HISTORY),               # 10
            ]
        )

        # --- BARRA SUPERIOR ---
        appbar = ft.AppBar(
            leading=ft.IconButton(icon=ft.Icons.MENU, icon_color="white", on_click=lambda _: page.open(drawer)),
            title=ft.Text("Início", size=22, color="white"),
            bgcolor="#b551c7",
            actions=[
                ft.Container(width=40, height=40, bgcolor="white", border_radius=50, margin=ft.Margin(0,0,10,0),
                             content=ft.IconButton(ft.Icons.LOGOUT, icon_color="#b551c7", icon_size=20, on_click=fechar_app)),
            ],
        )

        def botao_cat(text, rota):
            return ft.ElevatedButton(
                content=ft.Text(text, size=20, color="white", weight="w500"),
                bgcolor="#b551c7", width=350, height=100, on_click=lambda _: page.go(rota)
            )

        # --- MONTAGEM DA PÁGINA ---
        page.views.append(
            ft.View(
                route="/",
                appbar=appbar,
                drawer=drawer, 
                padding=0,
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        controls=[
                            ft.Stack([
                                ft.Container(height=400, image=ft.DecorationImage(src="img/degrade_home.gif", fit=ft.ImageFit.COVER)),
                                ft.Container(alignment=ft.alignment.center, padding=ft.padding.only(top=150), 
                                             content=ft.TextField(hint_text="Pesquisa ...", width=500, border_radius=30, bgcolor="white", border_color="transparent")),
                            ]),
                            
                           
                            ft.Container(
                                padding=40,
                                width=page.width,
                                content=ft.Column([self.loading_indicator, self.container_graficos], horizontal_alignment="center")
                            ),

                            
                            ft.Container(
                                padding=ft.padding.only(bottom=60),
                                content=ft.Column([
                                    ft.Row([botao_cat("🏫 Salas / Labs", "/sala"), botao_cat("💻 Informática", "/informatica"), botao_cat("🎤 Áudio / Vídeo", "/audio")], alignment="center"),
                                    ft.Row([botao_cat("❄️ Infraestrutura", "/infraestrutura"), botao_cat("🪑 Mobiliário", "/mobiliario"), botao_cat("🖋️ Material Escritório", "/material")], alignment="center"),
                                    ft.Row([botao_cat("🛡️ Segurança", "/seguranca"), botao_cat("... Outros", "/outros")], alignment="center"),
                                ], spacing=20)
                            )
                        ]
                    )
                ]
            )
        )

        async def carregar_tudo():
            await asyncio.sleep(0.8)
            try:
                # Grafico 1: emprestimos
                df1 = pd.DataFrame([{"Cat": "Eletrônicos", "Qtd": 15}, {"Cat": "Móveis", "Qtd": 5}, {"Cat": "Periféricos", "Qtd": 20}])
                fig1 = px.bar(df1, x="Cat", y="Qtd", color="Cat", title="Empréstimos Diários", color_discrete_sequence=["#d2b0e9", "#e067c7", "#b551c7"])
                
                # Grafico 2: ativos/inativos
                df2 = pd.DataFrame({"Status": ["Ativos", "Inativos"], "Qtd": [10, 3]})
                fig2 = px.pie(df2, names="Status", values="Qtd", title="Status Geral", color_discrete_sequence=["#d2b0e9", "#b551c7"])
                
                # Grafico 3: pendentes
                df3 = pd.DataFrame([{"Cat": "Livros", "v": 8}, {"Cat": "Ferramentas", "v": 3}])
                fig3 = px.bar(df3, x="Cat", y="v", title="Itens Pendentes", color_discrete_sequence=["#d2b0e9"])

                for f in [fig1, fig2, fig3]:
                    f.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320, margin=dict(l=10, r=10, t=50, b=10))

                self.container_graficos.controls.clear()
                
                
                for fig in [fig1, fig2, fig3]:
                    self.container_graficos.controls.append(
                        ft.Container(
                            content=PlotlyChart(fig, expand=True),
                            width=380, bgcolor="white", border_radius=15, padding=10,
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, "black"))
                        )
                    )

                self.loading_indicator.visible = False
                self.container_graficos.visible = True
                page.update()
            except Exception as e:
                print(f"Erro: {e}")

        page.run_task(carregar_tudo)
        page.update()