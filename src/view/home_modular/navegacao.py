import flet as ft
import os


def criar_navigation(page: ft.Page):
    """
    Cria toda a navegação da Home:
    - AppBar
    - Drawer
    - SnackBar de ajuda
    - Funções de sair
    """

    # ================== FECHAR APP ==================
    def fechar_app(e=None):
        try:
            page.window.destroy()
        except Exception:
            try:
                page.window_destroy()
            except Exception:
                os._exit(0)

    # ================== SNACKBAR AJUDA ==================
    def fechar_snack(e=None):
        snack_bar.open = False
        page.update()

    snack_bar = ft.SnackBar(
        content=ft.Text(
            "Precisa de ajuda? Use a barra de pesquisa para encontrar itens rapidamente. "
            "Os gráficos acima mostram um resumo visual das categorias cadastradas."
        ),
        action="OK",
        on_action=fechar_snack,
        duration=9000,
    )

    page.overlay.append(snack_bar)

    def abrir_ajuda(e=None):
        snack_bar.open = True
        page.update()

    # ================== DRAWER ==================
    drawer = ft.NavigationDrawer(
        on_change=lambda e: page.go([
            "/",                # 0
            "/cadastro",        # 1
            "/emprestimo",      # 2
            "/devolucao",       # 3
            "/imprimir_relatório",       # 4
        ][e.control.selected_index]),
        controls=[
            ft.NavigationDrawerDestination(label="Início", icon=ft.Icons.HOME),
            ft.NavigationDrawerDestination(label="Cadastrar Item", icon=ft.Icons.ADD_CIRCLE),
            ft.NavigationDrawerDestination(label="Empréstimo", icon=ft.Icons.WIDGETS),
            ft.NavigationDrawerDestination(label="Devolução", icon=ft.Icons.REPLAY),
            ft.NavigationDrawerDestination(label="Relatório", icon=ft.Icons.DOWNLOAD),
        ],
    )

    # ================== APPBAR ==================
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
        title=ft.Text("Menu", size=22, color=ft.Colors.WHITE),
        bgcolor="#b551c7",
        actions=[
            ft.Container(
                width=40,
                height=40,
                bgcolor="white",
                border_radius=50,
                margin=ft.Margin(0, 0, 10, 0),
                ink=True,
                alignment=ft.alignment.center,
                content=ft.Icon(ft.Icons.LOGOUT, color="#b551c7", size=30),
                on_click=fechar_app,
            ),
            ft.Container(
                width=40,
                height=40,
                bgcolor="white",
                border_radius=50,
                margin=ft.Margin(0, 0, 20, 0),
                ink=True,
                alignment=ft.alignment.center,
                content=ft.Icon(ft.Icons.QUESTION_MARK, color="#b551c7", size=30),
                on_click=abrir_ajuda,
            ),
        ],   
    )

    return appbar, drawer



'''import flet as ft
import os


def criar_navigation(page: ft.Page):
    if hasattr(page, "_navigation_ready"):
        return  # 🔒 impede recriação

    page._navigation_ready = True

    # ============ FECHAR APP ============
    def fechar_app(e):
        os._exit(0)

    # ============ SNACKBAR ============
    snack_bar = ft.SnackBar(
        content=ft.Text(
            "Precisa de ajuda? Use a barra de pesquisa para encontrar itens rapidamente. "
            "Os gráficos acima mostram um resumo visual das categorias cadastradas."
        ),
        action="OK",
        duration=6000,
    )
    page.overlay.append(snack_bar)

    def abrir_ajuda(e):
        snack_bar.open = True
        page.update()

    # ============ DRAWER ============
    drawer = ft.NavigationDrawer(
        on_change=lambda e: page.go([
            "/", "/cadastro", "/emprestimo", "/devolucao", "/relatorio"
        ][e.control.selected_index]),
        controls=[
            ft.NavigationDrawerDestination(label="Início", icon=ft.Icons.HOME),
            ft.NavigationDrawerDestination(label="Cadastrar Item", icon=ft.Icons.ADD),
            ft.NavigationDrawerDestination(label="Empréstimo", icon=ft.Icons.WIDGETS),
            ft.NavigationDrawerDestination(label="Devolução", icon=ft.Icons.REPLAY),
            ft.NavigationDrawerDestination(label="Relatório", icon=ft.Icons.DOWNLOAD),
        ],
    )

    page.drawer = drawer  # 🔴 ESSENCIAL

    # ============ APPBAR ============
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            icon_color="white",
            icon_size=30,
            on_click=lambda _: page.open(drawer),
        ),
        title=ft.Text("Menu", size=22, color="white"),
        bgcolor="#b551c7",
        actions=[
            ft.IconButton(
                icon=ft.Icons.QUESTION_MARK,
                icon_color="#b551c7",
                bgcolor="white",
                tooltip="Ajuda",
                on_click=abrir_ajuda,
            ),
            ft.IconButton(
                icon=ft.Icons.LOGOUT,
                icon_color="#b551c7",
                bgcolor="white",
                tooltip="Sair",
                on_click=fechar_app,
            ),
        ],
    )'''
