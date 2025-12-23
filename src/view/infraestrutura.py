import flet as ft
import asyncio

from src.model.model import separar_o_retorno_por_variavel, pegar_linhas_da_view_do_banco


class infraestrutura_view:
    def __init__(self):
        pass

    def main(self, page: ft.Page):
        page.title = "Infraestrutura"
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        # ================= AJUDA =================
        def fechar_snack():
            snack_bar.open = False
            page.update()

        snack_bar = ft.SnackBar(
            content=ft.Text("Use o filtro para ver os itens disponíveis e/ou indisponíveis."),
            action="OK",
            on_action=lambda _: fechar_snack(),
            duration=9000,
        )

        page.overlay.append(snack_bar)

        def abrir_ajuda(e):
            snack_bar.open = True
            page.update()
        
        # ================= DRAWER =================
        def navegar(index):
            rotas = [
                "/audio",
                "/sala",
                "/informatica",
                "/infraestrutura",
                "/mobiliario",
                "/material",
                "/seguranca",
                "/outros",
                "/",  
            ]
            page.go(rotas[index])

        drawer = ft.NavigationDrawer(
            selected_index=0,  # define item inicial
            on_change=lambda e: navegar(drawer.selected_index),  
            controls=[
                ft.NavigationDrawerDestination(label="Áudio / Vídeo", icon=ft.Icons.VIDEO_CAMERA_FRONT),
                ft.NavigationDrawerDestination(label="Sala / Laboratório", icon=ft.Icons.BIOTECH),
                ft.NavigationDrawerDestination(label="Informática", icon=ft.Icons.LAPTOP),
                ft.NavigationDrawerDestination(label="Infraestrutura", icon=ft.Icons.CABLE),
                ft.NavigationDrawerDestination(label="Mobiliário", icon=ft.Icons.WEEKEND),
                ft.NavigationDrawerDestination(label="Material de Escritório", icon=ft.Icons.EDIT),
                ft.NavigationDrawerDestination(label="Segurança", icon=ft.Icons.SECURITY),
                ft.NavigationDrawerDestination(label="Outros", icon=ft.Icons.MISCELLANEOUS_SERVICES),
                ft.NavigationDrawerDestination(label="Início", icon=ft.Icons.HOME),
            ]
        )

        # ================= DADOS =================
        linhas = pegar_linhas_da_view_do_banco("visao_infraestrutura")
        separar_linhas_categoria = separar_o_retorno_por_variavel(linhas)

        # ================= GRID =================
        grid = ft.GridView(expand=True, max_extent=240, spacing=20, run_spacing=20)

        def criar_card(produto):
            nome = produto["Produto"]
            status = produto["Status"].strip().lower()
            unidades = produto["Unidades"]

            if status == "ativo":
                cor_botao = ft.Colors.GREEN_400
                texto_botao = "Disponível"
            else:
                cor_botao = ft.Colors.RED_400
                texto_botao = "Indisponível"

            return ft.Container(
                width=250,
                padding=15,
                border_radius=12,
                bgcolor="#fffefe",
                shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color="#00000020"),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(nome, weight=ft.FontWeight.BOLD, size=14),
                        ft.ElevatedButton(text=texto_botao, bgcolor=cor_botao, color=ft.Colors.WHITE),
                        ft.Text(f"Unidades: {unidades}"),
                    ],
                ),
            )

        # ================= FILTRO =================
        def filtrar_status(status):
            grid.controls.clear()

            for p in separar_linhas_categoria:
                if status == "todos":
                    grid.controls.append(criar_card(p))
                elif status == "ativo" and p["Status"].strip().lower() == "ativo":
                    grid.controls.append(criar_card(p))
                elif status == "indisponível" and p["Status"].strip().lower() != "ativo":
                    grid.controls.append(criar_card(p))

            page.update()

        filtro_popup = ft.PopupMenuButton(
            icon=ft.Icons.FILTER_ALT,
            icon_color="#b551c7",
            items=[
                ft.PopupMenuItem(text="Mostrar todos", on_click=lambda _: filtrar_status("todos")),
                ft.PopupMenuItem(text="Disponíveis", on_click=lambda _: filtrar_status("ativo")),
                ft.PopupMenuItem(text="Indisponíveis", on_click=lambda _: filtrar_status("indisponível")),
            ],
        )

        # ================= APPBAR =================
        appbar = ft.AppBar(
            leading=ft.Container(
                width=50,
                height=50,
                bgcolor="#b551c7",
                border_radius=50,
                content=ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_size=30,
                    icon_color="white",
                    on_click=lambda _: page.open(drawer),
                ),
            ),
            title=ft.Text("", size=22, color=ft.Colors.WHITE),
            bgcolor="#b551c7",
            actions=[
                ft.Container(
                    width=40,
                    height=40,
                    bgcolor="white",
                    border_radius=50,
                    margin=ft.Margin(0, 0, 10, 0),
                    content=filtro_popup,
                ),
                ft.Container(
                    width=40,
                    height=40,
                    bgcolor="white",
                    border_radius=50,
                    ink=True,
                    margin=ft.Margin(0, 0, 20, 0),
                    on_click=abrir_ajuda,
                    content=ft.Icon(ft.Icons.QUESTION_MARK, color="#b551c7", size=30),
                ),
            ],
        )

        # ================= VIEW =================
        page.views.append(
            ft.View(
                route="/audio",
                appbar=appbar,
                drawer=drawer,
                controls=[
                    ft.Container(
                        expand=True,
                        bgcolor="#ffffff",
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
                                        src="img/audio_video.gif",
                                        fit=ft.ImageFit.COVER,
                                    ),
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
                                                color="#00000020",
                                            ),
                                            content=ft.Column(
                                                expand=True,
                                                spacing=25,
                                                horizontal_alignment="center",
                                                controls=[grid],
                                            ),
                                        )
                                    ],
                                ),
                            ],
                        ),
                    )
                ],
            )
        )

        # ================= POPULA GRID =================
        async def popular_grid_lentamente():
            for p in separar_linhas_categoria:
                grid.controls.append(criar_card(p))
                page.update()
                await asyncio.sleep(0.2)

        page.run_task(popular_grid_lentamente)
