import flet as ft

class devolucao_view:
    def __init__(self):
        pass

    def main(self, page: ft.Page):
        page.title = "Devolução"
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        #Ajuda ------------------------------------------------------------------------------------------------------------
        def fechar_snack():
            snack_bar.open = False
            page.update()
        
        snack_bar = ft.SnackBar(
                content=ft.Text("Use o filtro para ver os itens disponíveis e/ou indisponíveis."),
                action="OK",
                on_action=lambda _: fechar_snack(),
                duration=9000 )
        
        page.overlay.append(snack_bar)

        def abrir_ajuda(e):
            snack_bar.open = True
            page.update()

        #Início Menu ---------------------------------------------------------------------------------------------------------------
        page.drawer = ft.NavigationDrawer(
            controls= [
                ft.NavigationDrawerDestination(
                    label= "Devolução", icon= ft.Icons.REPLAY
                ),
                ft.NavigationDrawerDestination(
                    label= "Cadastrar Item", icon= ft.Icons.ADD_CIRCLE
                ),
                ft.NavigationDrawerDestination(
                    label= "Empréstimo", icon= ft.Icons.WIDGETS
                ),
                ft.NavigationDrawerDestination(
                    label= "Ajustar Empréstimo", icon= ft.Icons.SETTINGS_OUTLINED
                ),
                ft.NavigationDrawerDestination(
                    label= "Imprimir Relatório", icon= ft.Icons.DOWNLOAD
                ),
                ft.NavigationDrawerDestination(
                    label= "Início", icon= ft.Icons.HOME
                )
            ]
        )

        #Barra de Menu ------------------------------------------------------------------------------------------------------------
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
            title= ft.Text("", size=22, color=ft.Colors.WHITE),
            bgcolor= "#b551c7",
            actions= [
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

        #Inicio dos Cards ---------------------------------------------------------------------------------------------------------
        
        
        #Início Filtro ------------------------------------------------------------------------------------------------------------
        

        #Estilização da Página ------------------------------------------------------------------------------------------------------------
        page.add(
            ft.Container(
                expand=True,
                bgcolor="#ffffff",
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Column(
                    [
                        ft.Container(
                            height=250,
                            expand=True,
                            image=ft.DecorationImage(
                                src="img/devolucao.gif",
                                fit=ft.ImageFit.COVER),
                        ),
                        
                        ft.Container(
                            padding= ft.Padding(30, 0, 30, 5),
                            
                        ),
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
    view = devolucao_view()
    view.main(page)

ft.app(target=main)