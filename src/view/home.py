import plotly.express as px

import flet as ft
from flet.plotly_chart import PlotlyChart

# tive que instalar o flet: pip install flet
# tive que atualizar o flet com: pip install "flet[all]==0.25.2" --upgrade
# tive que instalar: pip install plotly
# tive que instalar: pip install --upgrade kaleido
# tive que instalar plotly.express: pip install "plotly[express]"
#tive que instalar o pandas: pip install pandas

class home_view:
    def __init__(self):
        pass

    def main(self, page: ft.Page):
        page.title = "Home"
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

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
                    label= "Ajustar Empréstimo", icon= ft.Icons.SETTINGS_OUTLINED
                ),
                ft.NavigationDrawerDestination(
                    label= "Imprimir Relatório", icon= ft.Icons.DOWNLOAD
                ),

            ]
        )

        #Barra de Pesquisa ---------------------------------------------------------------------------------------------------------------
        pesquisa = ft.TextField(
            hint_text= "Pesquisa ...",
            prefix_icon = ft.Icons.SEARCH,
            border_radius= 30,
            width= 500,
            filled= True,
            bgcolor= "white",
            border_color= "transparent",
        )

        #Gráfico de Barras ---------------------------------------------------------------------------------------------------------------
        dadosb = {
            "Item": ["Item 1", "Item 2", "Item 3", "Item 4"],
            "Valor": [8, 12, 16, 20]
        }

        barra = px.bar(
            dadosb, 
            x="Item", 
            y="Valor", 
            title="Gráfico de Barras", 
            color="Item",
            color_discrete_sequence=["#d2b0e9", "#e067c7", "#b551c7","#00357a"])

        grafico_barra =  ft.Container(
            content= PlotlyChart(barra, expand=True),
            width= 425,
            height= 375
        )

        #Gráfico de Pizza ---------------------------------------------------------------------------------------------------------------
        dadosp = {
            "Item": ["Item 5", "Item 6", "Item 7", "Item 8"],
            "Percentual": [8, 12, 16, 20]
        }

        pizza = px.pie(
            dadosp,
            names= "Item", 
            values= "Percentual", 
            title= "Distribuição",
            color_discrete_sequence=["#d2b0e9", "#e067c7", "#b551c7","#00357a"])

        grafico_pizza =  ft.Container(
            content= PlotlyChart(pizza, expand=True),
            width= 425,
            height= 375
        )

        #Gráfico de Barras Empilhadas ---------------------------------------------------------------------------------------------------------------
        dadose = {
            "Item": ["Item 5", "Item 6", "Item 7", "Item 8"],
            "Série 9": [8, 12, 16, 20],
            "Série 10": [8, 12, 16, 20],
            "Série 11": [8, 12, 16, 20]
        }

        empilhado = px.bar(
            dadose, 
            x= "Item", 
            y=["Série 9", "Série 10", "Série 11"], 
            title= "Barras Empilhadas",
            color_discrete_sequence=["#d2b0e9", "#e067c7","#00357a"])
 
        grafico_empilhado =  ft.Container(
            content= PlotlyChart(empilhado, expand=True),
            width= 425,
            height= 375
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
                    margin = ft.Margin(0,0,10,0),
                    content= ft.Icon(
                        ft.Icons.PERSON,
                        color= "#b551c7",
                        size= 30
                    ),
                    on_click= lambda _: print("Perfil clicado!")
                ),
                ft.Container(
                    width= 40,
                    height= 40,
                    bgcolor= "white",
                    border_radius= 50,
                    ink= True,
                    margin = ft.Margin(0,0,20,0),
                    on_click= abrir_ajuda,
                    content= ft.Icon(
                        ft.Icons.QUESTION_MARK,
                        color= "#b551c7",
                        size= 30
                    )
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
                                    alignment = ft.alignment.center,
                                    content= pesquisa
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
                            ]
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


def main(page: ft.Page):
    view = home_view()
    view.main(page)

ft.app(target=main)