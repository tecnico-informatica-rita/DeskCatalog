# view.py
"""
Camada View:
- Contém todas as funções responsáveis pela interação com o usuário.
- Funções de exibição e de obtenção de dados.
"""
import flet as ft

#Início BD ---------------------------------------------------------------------------------------------------------------
separar_linhas_categoria_informatica = [
    {"Produto": "Mouse Gamer", "Status": "Disponível", "Unidades": 12},
    {"Produto": "Teclado Mecânico", "Status": "Indisponível", "Unidades": 0},
    {"Produto": "Monitor 24\"", "Status": "Disponível", "Unidades": 5},
    {"Produto": "Mouse Gamer", "Status": "Disponível", "Unidades": 12},
    {"Produto": "Teclado Mecânico", "Status": "Indisponível", "Unidades": 0},
    {"Produto": "Monitor 24\"", "Status": "Disponível", "Unidades": 5},
    {"Produto": "Mouse Gamer", "Status": "Disponível", "Unidades": 12},
    {"Produto": "Teclado Mecânico", "Status": "Indisponível", "Unidades": 0},
    {"Produto": "Monitor 24\"", "Status": "Disponível", "Unidades": 5}
    ]

class ItensView:
    def __init__(self):
        pass

    def main(self, page: ft.Page):
        page.title = "Sala/Laboratório"
        page.window_resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        #Ajuda ------------------------------------------------------------------------------------------------------------
        def abrir_ajuda(e):
            page.dialog = dlg  
            dlg.open = True
            page.update()

        def fechar_dialog():
            dlg.open = False
            page.update()
        
        dlg = ft.AlertDialog(
            modal = True,
            title=ft.Text("Ajuda"),
            content=ft.Text("Use o filtro para ver os itens disponíveis e/ou indisponíveis."),
            actions=[
                ft.TextButton("OK", on_click= fechar_dialog)
            ],
        )

        #Início Menu ---------------------------------------------------------------------------------------------------------------
        page.drawer = ft.NavigationDrawer(
            controls= [
                ft.NavigationDrawerDestination(
                    label= "Início", icon= ft.Icons.HOME
                ),
                ft.NavigationDrawerDestination(
                    label= "Informática", icon= ft.Icons.LAPTOP
                ),
                ft.NavigationDrawerDestination(
                    label= "Áudio / Vídeo", icon= ft.Icons.VIDEO_CAMERA_FRONT
                ),
                ft.NavigationDrawerDestination(
                    label= "Infraestrutura", icon= ft.Icons.CABLE
                ),
                ft.NavigationDrawerDestination(
                    label= "Mobiliário", icon= ft.Icons.WEEKEND
                ),
                ft.NavigationDrawerDestination(
                    label= "Material de Escritório", icon= ft.Icons.EDIT
                ),
                ft.NavigationDrawerDestination(
                    label= "Segurança", icon= ft.Icons.SECURITY
                ),
                ft.NavigationDrawerDestination(
                    label= "Outros", icon= ft.Icons.MISCELLANEOUS_SERVICES
                )
            ]
        )

        #Filtro ------------------------------------------------------------------------------------------------------------
        filtro_popup = ft.PopupMenuButton(
            icon= ft.Icons.FILTER_ALT,
            icon_color= "#b551c7",
            items = [
                ft.PopupMenuItem(text= "Mostrar todos", on_click= lambda _: filtrar_status("todos")),
                ft.PopupMenuItem(text= "Disponíveis", on_click= lambda _: filtrar_status("disponível")),
                ft.PopupMenuItem(text= "Indisponíveis", on_click= lambda _: filtrar_status("indisponível"))
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
                    margin = ft.Margin(0,0,10,0),
                    content= filtro_popup
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

        #Inicio dos Cards ---------------------------------------------------------------------------------------------------------
        def criar_card(produto, on_click_disponivel=None, on_click_indisponivel=None):
            nome = produto["Produto"]
            status = produto["Status"].lower()
            unidades = produto["Unidades"]
        
            if status == "disponível":
                cor_botao = ft.Colors.GREEN_400
                texto_botao = "Disponível"
                on_click = on_click_disponivel
            else:
                cor_botao = ft.Colors.RED_400
                texto_botao = "Indisponível"
                on_click = on_click_indisponivel
 
            return ft.Container(
                width=250,
                padding=15,
                border_radius=12,
                bgcolor=ft.Colors.GREY_50,
                shadow=ft.BoxShadow(blur_radius=12, spread_radius=1, color="#00000020"),
                content=ft.Column([
                    ft.Text(nome, weight=ft.FontWeight.BOLD, size=14),

                    #STATUS
                    ft.ElevatedButton(
                        text=texto_botao,
                        bgcolor=cor_botao,
                        color=ft.Colors.WHITE,
                        on_click=on_click
                    ),
        
                    ft.Text(f"Unidades: {unidades}"),
                ])
            )
        
        grid = ft.GridView(
            expand=True,
            max_extent=240,
            spacing=20,
            run_spacing=20
        )

        for p in separar_linhas_categoria_informatica:
            grid.controls.append(criar_card(p))
        
        #Início Filtro ------------------------------------------------------------------------------------------------------------
        def filtrar_status(status):
            grid.controls.clear()

            for p in separar_linhas_categoria_informatica:
                if status == "todos":
                    grid.controls.append(criar_card(p))
                else:
                    if p["Status"].lower() == status:
                        grid.controls.append(criar_card(p))
            page.update()

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
                                src="img/sala_laboratorio.gif",
                                fit=ft.ImageFit.COVER),
                        ),
                        
                        ft.Container(
                            padding= ft.Padding(30, 0, 30, 5),
                            content= grid
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
    view = ItensView()
    view.main(page)

ft.app(target=main)
