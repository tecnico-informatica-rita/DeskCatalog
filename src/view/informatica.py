import flet as ft
from src.model.model import separar_o_retorno_por_variavel
import asyncio
import functools 


class informatica_view:
    def __init__(self):
        pass

    def main(self, page: ft.Page):
        page.title = "Informática"
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        def fechar_snack():
            page.snack_bar.open = False
            page.update()
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Use o filtro para consultar a disponibilidade dos equipamentos de informática."),
            action="OK",
            on_action=lambda _: fechar_snack(),
            duration=9000
        )
        page.overlay.append(page.snack_bar)
        
        def abrir_ajuda(e):
            page.snack_bar.open = True
            page.update()

        page.drawer = ft.NavigationDrawer(
            controls= [
                ft.NavigationDrawerDestination(
                    label="Informática", icon=ft.Icons.LAPTOP
                ),
                ft.NavigationDrawerDestination(
                    label="Sala / Laboratório", icon=ft.Icons.BIOTECH
                ),
                ft.NavigationDrawerDestination(
                    label="Áudio / Vídeo", icon=ft.Icons.VIDEO_CAMERA_FRONT
                ),
                ft.NavigationDrawerDestination(
                    label="Infraestrutura", icon=ft.Icons.CABLE
                ),
                ft.NavigationDrawerDestination(
                    label="Mobiliário", icon=ft.Icons.WEEKEND
                ),
                ft.NavigationDrawerDestination(
                    label="Material de Escritório", icon=ft.Icons.EDIT
                ),
                ft.NavigationDrawerDestination(
                    label="Segurança", icon=ft.Icons.SECURITY
                ),
                ft.NavigationDrawerDestination(
                    label="Outros", icon=ft.Icons.MISCELLANEOUS_SERVICES
                ),
                ft.NavigationDrawerDestination(
                    label="Início", icon=ft.Icons.HOME
                )
            ]
        )

        filtro_popup = ft.PopupMenuButton(
            icon=ft.Icons.FILTER_ALT,
            icon_color="#b551c7",
            items=[
                ft.PopupMenuItem(text="Mostrar todos", on_click=lambda _: filtrar_status("todos")),
                ft.PopupMenuItem(text="Disponíveis", on_click=lambda _: filtrar_status("ativo")),
                ft.PopupMenuItem(text="Indisponíveis", on_click=lambda _: filtrar_status("indisponível"))
            ]
        )

        page.appbar = ft.AppBar(
            leading=ft.Container(
                width=50,
                height=50,
                bgcolor="#b551c7",
                border_radius=50,
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.MENU,
                            icon_size=30,
                            icon_color="white",
                            on_click=lambda _: page.open(page.drawer)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ),
            title=ft.Text("Informática", size=22, color=ft.Colors.WHITE),
            bgcolor="#b551c7",
            actions=[
                ft.Container(
                    width=40,
                    height=40,
                    bgcolor="white",
                    border_radius=50,
                    margin=ft.Margin(0, 0, 10, 0),
                    content=filtro_popup
                ),
                ft.Container(
                    width=40,
                    height=40,
                    bgcolor="white",
                    border_radius=50,
                    ink=True,
                    margin=ft.Margin(0, 0, 20, 0),
                    on_click=abrir_ajuda,
                    content=ft.Icon(
                        ft.Icons.QUESTION_MARK,
                        color="#b551c7",
                        size=30
                    )
                )
            ]
        )

        linhas_teste = [
            ("Notebook Dell", "ativo", 5),
            ("Mouse Logitech", "indisponível", 12),
            ("Teclado Microsoft", "ativo", 7),
            ("Monitor LG", "indisponível", 3),
            ("Impressora HP", "ativo", 2),
            ("Scanner Canon", "ativo", 4),
            ("Webcam Logitech", "indisponível", 6),
            ("Headset HyperX", "ativo", 10),
            ("Estabilizador APC", "ativo", 8),
            ("SSD Samsung 1TB", "indisponível", 5),
            ("Pendrive SanDisk 64GB", "ativo", 20),
            ("HD Externo Seagate", "indisponível", 7),
            ("Cabo HDMI", "ativo", 15),
            ("Roteador TP-Link", "ativo", 3),
            ("Switch Cisco", "indisponível", 2),
            ("Placa de Vídeo NVIDIA", "indisponível", 1),
            ("Memória RAM 16GB", "ativo", 12),
            ("Fonte Corsair 600W", "ativo", 4),
            ("Gabinete Cooler Master", "indisponível", 3),
            ("Mouse Pad SteelSeries", "ativo", 9)
        ]
        
        separar_linhas_categoria_informatica = separar_o_retorno_por_variavel(linhas_teste)
        
        def criar_card(produto, on_click_disponivel=None, on_click_indisponivel=None):
            nome = produto["Produto"]
            status = produto["Status"].strip().lower()
            unidades = produto["Unidades"]
        
            if status == "ativo":
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

        async def popular_grid_lentamente(page, grid, produtos):
            for p in produtos:
                grid.controls.append(criar_card(p))
                page.update()
                await asyncio.sleep(0.50)

        def filtrar_status(status):
            grid.controls.clear()

            for p in separar_linhas_categoria_informatica:
                if status == "todos":
                    grid.controls.append(criar_card(p))
                elif status == "ativo":
                    if p["Status"].strip().lower() == "ativo":
                        grid.controls.append(criar_card(p))
                elif status == "indisponível":
                    if p["Status"].strip().lower() != "ativo":
                        grid.controls.append(criar_card(p))
            page.update()

        page.add(
            ft.Container(
                expand=True,
                bgcolor="#ffffff",
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment="center",
                    spacing=25,
                    controls=[
                        ft.Container(
                            height=250,
                            expand=True,
                            image=ft.DecorationImage(
                                src="img/informatica.gif",
                                fit=ft.ImageFit.COVER),
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=1080,
                                    bgcolor="white",
                                    border_radius=40,
                                    padding=40,
                                    margin=ft.Margin(0, -60, 0, 0),
                                    shadow=ft.BoxShadow(
                                        blur_radius=20,
                                        spread_radius=5,
                                        color="#fffff",
                                    ),
                                    content=ft.Column(
                                        expand=True,
                                        spacing=25,
                                        horizontal_alignment="center",
                                        controls=[grid],
                                    )
                                )
                            ],
                        )
                    ]
                )
            )
        )
        

        task = functools.partial(popular_grid_lentamente, page, grid, separar_linhas_categoria_informatica)
        page.run_task(task)


def main(page: ft.Page):
    view = informatica_view()
    view.main(page)

ft.app(target=main)