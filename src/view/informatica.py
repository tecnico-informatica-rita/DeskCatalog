import flet as ft
from src.model.model import separar_o_retorno_por_variavel
import asyncio
import functools
from src.controller.controller import pegar_linhas_da_view_do_banco


class informatica_view:
    def __init__(self):
        pass

    def main(self, page: ft.Page):
        page.title = "Informática"
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        # ================= SNACKBAR =================
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

        # ================= MENU (ROTAS) =================
        def navegar_menu(e):
            rotas = {
                0: "/",
                1: "/cadastrar-item",
                2: "/emprestimo",
                3: "/devolucao",
                4: "/relatorio",
            }
            if e.control.selected_index in rotas:
                page.go(rotas[e.control.selected_index])

        page.drawer = ft.NavigationDrawer(
            on_change=navegar_menu,
            controls=[
                ft.NavigationDrawerDestination(label="Início", icon=ft.Icons.HOME),
                ft.NavigationDrawerDestination(label="Cadastrar Item", icon=ft.Icons.ADD_CIRCLE),
                ft.NavigationDrawerDestination(label="Empréstimo", icon=ft.Icons.WIDGETS),
                ft.NavigationDrawerDestination(label="Devolução", icon=ft.Icons.REPLAY),
                ft.NavigationDrawerDestination(label="Relatório", icon=ft.Icons.DOWNLOAD),
            ]
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
                ft.PopupMenuItem(text="Indisponíveis", on_click=lambda _: filtrar_status("indisponível"))
            ]
        )

        # ================= APPBAR =================
        page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.MENU,
                icon_size=30,
                icon_color="white",
                on_click=lambda _: page.open_drawer()  # CORRETO para abrir drawer
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
                    content=ft.Icon(ft.Icons.QUESTION_MARK, color="#b551c7", size=30)
                )
            ]
        )

        # ================= DADOS =================
        linhas = pegar_linhas_da_view_do_banco('visao_informatica')
        separar_linhas_categoria = separar_o_retorno_por_variavel(linhas)

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
                bgcolor="#f5f5f5",
                shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color="#00000020"),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(nome, weight=ft.FontWeight.BOLD, size=14),
                        ft.ElevatedButton(text=texto_botao, bgcolor=cor_botao, color=ft.Colors.WHITE, on_click=on_click),
                        ft.Text(f"Unidades: {unidades}")
                    ]
                )
            )

        grid = ft.GridView(expand=True, max_extent=240, spacing=20, run_spacing=20)

        async def popular_grid_lentamente(page, grid, produtos):
            for p in produtos:
                grid.controls.append(criar_card(p))
                page.update()
                await asyncio.sleep(0.3)

        # ================= VIEW =================
        page.views.append(
            ft.View(
                route="/informatica",
                controls=[
                    ft.Container(
                        expand=True,
                        bgcolor="#f0f0f0",
                        content=ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            horizontal_alignment="center",
                            spacing=20,
                            controls=[
                                # cabeçalho roxo como Home
                                ft.Container(
                                    height=180,
                                    expand=True,
                                    padding=ft.Padding(20, 20, 20, 20),
                                    alignment=ft.alignment.center,
                                    bgcolor="#b551c7",
                                    border_radius=20,
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("Informática", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                                        ]
                                    )
                                ),
                                # Grid de cards
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(
                                            width=1080,
                                            bgcolor="white",
                                            border_radius=40,
                                            padding=40,
                                            margin=ft.Margin(0, -60, 0, 0),
                                            shadow=ft.BoxShadow(blur_radius=20, spread_radius=5, color="#00000020"),
                                            content=ft.Column(
                                                expand=True,
                                                spacing=25,
                                                horizontal_alignment="center",
                                                controls=[grid]
                                            )
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )

        # ================= POPULA GRID =================
        task = functools.partial(popular_grid_lentamente, page, grid, separar_linhas_categoria)
        page.run_task(task)

        # ================= ABRE VIEW AUTOMÁTICA =================
        page.go("/informatica")

