import pandas as pd
import plotly.express as px
import flet as ft
from flet.plotly_chart import PlotlyChart
from view.pesquisa import pagina_resultados

# tive que instalar o flet: pip install flet
# tive que atualizar o flet com: pip install "flet[all]==0.25.2" --upgrade
# tive que instalar: pip install plotly
# tive que instalar: pip install --upgrade kaleido
# tive que instalar plotly.express: pip install "plotly[express]"
# tive que instalar o pandas: pip install pandas

class home_view:
    def __init__(self, conn):
        self.conn = conn

    def main_home(self, page: ft.Page):
        page.title = "Home"
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        def rota_mudou(e):
            if page.route == "/":
                page.views.clear()
                page.views.append(ft.View("/", controls=page.controls))
            page.update()

        page.on_route_change = rota_mudou

        #Produtos de Teste ------------------------------------------------------------------------------------------------------------
        produtos_por_categoria = {
            "Eletrônicos": ["Mouse Gamer", "Teclado Mecânico", "Monitor"],
            "Móveis": ["Cadeira", "Mesa de Escritório"],
            "Acessórios": ["Fone de Ouvido", "Cabo"]
        }

        #Pesquisa de Produtos ---------------------------------------------------------------------------------------------------------------
        def enviar_pesquisa(e):
            texto = pesquisa.value.strip()
            if texto != "":
                pagina_resultados(page, texto, produtos_por_categoria)

        pesquisa = ft.TextField(
            hint_text="Pesquisa ...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=30,
            width=500,
            filled=True,
            bgcolor="white",
            border_color="transparent",
            on_submit=enviar_pesquisa
        )
        
        #Ajuda ------------------------------------------------------------------------------------------------------------
        def fechar(e):
            try:
                page.window.destroy()
            except AttributeError:
                try:
                    page.window_destroy()
                except Exception:
                    import os
                    os._exit(0)

        #Ajuda ------------------------------------------------------------------------------------------------------------
        def fechar_snack():
            snack_bar.open = False
            page.update()
        
        snack_bar = ft.SnackBar(
                content=ft.Text("Precisa de ajuda? Use a barra de pesquisa para encontrar itens rapidamente. Os gráficos acima mostram um resumo visual das categorias cadastradas."),
                action="OK",
                on_action=lambda _: fechar_snack(),
                duration=9000 )
        
        page.overlay.append(snack_bar)

        def abrir_ajuda(e):
            snack_bar.open = True
            page.update()

        #Funções no Menu ---------------------------------------------------------------------------------------------------------------
        page.drawer = ft.NavigationDrawer(
            controls= [
                ft.NavigationDrawerDestination(
                    label= "Início", icon= ft.Icons.HOME
                ),
                ft.NavigationDrawerDestination(
                    label= "Cadastrar Item", icon= ft.Icons.ADD_CIRCLE
                ),
                ft.NavigationDrawerDestination(
                    label= "Empréstimo", icon= ft.Icons.WIDGETS
                ),
                ft.NavigationDrawerDestination(
                    label= "Devolução", icon= ft.Icons.REPLAY
                ),
                ft.NavigationDrawerDestination(
                    label= "Relatório", icon= ft.Icons.DOWNLOAD
                )
            ]
        )

        #Gráfico de Barras ---------------------------------------------------------------------------------------------------------------
        dadosb = [ 
            {"Categoria": "Eletrônicos", "Qtd": 15},
            {"Categoria": "Móveis", "Qtd": 5},
            {"Categoria": "Periféricos", "Qtd": 20}
        ]

        df_barra = pd.DataFrame(dadosb)
        barra = px.bar(
            df_barra, 
            x="Categoria",      
            y="Qtd",             
            title="Empréstimos Diários por Categoria", 
            color="Categoria",   
            color_discrete_sequence=["#d2b0e9", "#e067c7", "#b551c7", "#00357a"]
        )

        grafico_barra = ft.Container(
            content=PlotlyChart(barra, expand=True),
            width=425,
            height=375
        )

        #Gráfico de Pizza ---------------------------------------------------------------------------------------------------------------
        dadosp = {
            "Ativos": 10, 
            "Inativos": 3}

        df_pizza = pd.DataFrame({
            "Item": list(dadosp.keys()),
            "Percentual": list(dadosp.values())
        })
        pizza = px.pie(
            df_pizza,
            names="Item",
            values="Percentual",
            title="Ativos e Inativos",
            color_discrete_sequence=["#d2b0e9", "#e067c7", "#b551c7", "#00357a"]
        )

        grafico_pizza = ft.Container(
            content=PlotlyChart(pizza, expand=True),
            width=425,
            height=375
        )

        #Gráfico de Barras Empilhadas ---------------------------------------------------------------------------------------------------------------
        dadose = [
            {"Categoria": "Livros", "Qtd": 8},
            {"Categoria": "Ferramentas", "Qtd": 3},
        ]

        df_barras = pd.DataFrame(dadose)

        empilhado = px.bar(
            df_barras,
            x="Categoria",
            y=[col for col in df_barras.columns if col != "Categoria"],  
            title="Itens Pendentes por Categoria",
            color_discrete_sequence=["#d2b0e9", "#e067c7", "#00357a"]
        )

        grafico_empilhado = ft.Container(
            content=PlotlyChart(empilhado, expand=True),
            width=425,
            height=375
        )
        #Início Menu ---------------------------------------------------------------------------------------------------------------
        page.appbar = ft.AppBar(
            leading= ft.Container(
                width= 50,
                height= 50,
                bgcolor= "#b551c7",
                border_radius= 50,
                content= ft.Row(
                    controls=[
                        ft.IconButton(
                        icon= ft.Icons.MENU,
                        icon_size= 30,
                        icon_color= "white",
                        on_click= lambda _: page.open(page.drawer)
                        )
                    ],
                    alignment= ft.MainAxisAlignment.CENTER,
                    vertical_alignment= ft.CrossAxisAlignment.CENTER
                ),
            ),
            title= ft.Text("Menu", size=22, color=ft.Colors.WHITE),
            bgcolor= "#b551c7",
            actions= [
                ft.Container(
                    width= 40,
                    height= 40,
                    bgcolor= "white",
                    border_radius= 50,
                    ink= True,
                    margin = ft.Margin(0,0,10,0),
                    content= ft.Icon(
                        ft.Icons.LOGOUT,
                        color= "#b551c7",
                        size= 30
                    ),
                    on_click= fechar
                ),
                ft.Container(
                    width= 40,
                    height= 40,
                    bgcolor= "white",
                    border_radius= 50,
                    ink= True,
                    margin = ft.Margin(0,0,20,0),
                    content= ft.Icon(
                        ft.Icons.QUESTION_MARK,
                        color= "#b551c7",
                        size= 30
                    ),
                    on_click= abrir_ajuda
                )
            ]
        )

        #Botões ---------------------------------------------------------------------------------------------------------------
        def botao_de_categoria(text):
            return ft.ElevatedButton(
                content= ft.Text(text, size= 22, color= ft.Colors.WHITE, weight= "w500"),
                bgcolor= "#b551c7",
                width= 350,
                height= 100,
            )

        salas = botao_de_categoria("🏫 Salas / Laboratórios")
        informatica = botao_de_categoria("💻 Informática")
        audio = botao_de_categoria("🎤 Áudio / Vídeo")
        infraestrutura = botao_de_categoria("❄️ Infraestrutura")
        mobiliario = botao_de_categoria("🪑 Mobiliário")
        escritorio = botao_de_categoria("🖋️ Material de Escritório")
        seguranca = botao_de_categoria("🛡️ Segurança")
        outros = botao_de_categoria("... Outros")
        
        #Estilização da Página ---------------------------------------------------------------------------------------------------------------
        page.add(
            ft.Container(
                expand=True,
                bgcolor="#ffffff",
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Column(
                    [
                        ft.Stack(
                            controls= [
                                ft.Container(
                                    height= 650,
                                    expand= True,
                                    image= ft.DecorationImage(
                                        src= "img/degrade_home.gif",
                                        fit= ft.ImageFit.COVER
                                    ),
                                ),
                                ft.Container(
                                    padding= 260,
                                    alignment = ft.alignment.top_center,
                                    content= ft.Column(
                                        [pesquisa],
                                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                        spacing= 5
                                    )
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        controls=[grafico_barra, grafico_pizza, grafico_empilhado],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=20
                                    ),
                                    top= 330,
                                    left=0,
                                    right=0,
                                    alignment=ft.alignment.center,
                                )
                            ],
                            clip_behavior=ft.ClipBehavior.NONE
                        ),
                        ft.Row([], alignment= ft.MainAxisAlignment.CENTER),
                        ft.Row([salas, informatica, audio], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        ft.Row([infraestrutura, mobiliario, escritorio], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        ft.Row([seguranca, outros], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,  
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                )
            )
        )

        return ft.Column(
                controls=[
                    ft.Text("Home funcionando", size=24),
                ]
            )
    
'''def main(page: ft.Page, conn):
    home = home_view(conn)
    home.main_home(page)

ft.app(target=main)'''