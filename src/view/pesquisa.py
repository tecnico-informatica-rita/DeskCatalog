import flet as ft

def pagina_resultados(page: ft.Page, termo_busca, produtos_por_categoria):
    def criar_card(nome, categoria):
        return ft.Container(
            width=250,
            padding=15,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            shadow=ft.BoxShadow(blur_radius=12, spread_radius=1, color="#ffffff"),
            content=ft.Column([
                ft.Text(nome, weight=ft.FontWeight.BOLD, size=14),
                ft.Text(f"Categoria: {categoria}"),
            ])
        )
    
    grid = ft.GridView(
        expand=True,
        max_extent=260,
        spacing=20,
        run_spacing=20
    )

    termo = termo_busca.lower().strip()
    encontrou = False

    for categoria, produtos in produtos_por_categoria.items():
        for produto in produtos:
            if termo in produto.lower():
                grid.controls.append(criar_card(produto, categoria))
                encontrou = True

    if not encontrou:
        grid.controls.append(
            ft.Text(f"Nenhum item encontrado para “{termo_busca}”.", size=18)
        )

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(label="Início", icon=ft.Icons.HOME),
            ft.NavigationDrawerDestination(label="Cadastrar Item", icon=ft.Icons.ADD_CIRCLE),
            ft.NavigationDrawerDestination(label="Empréstimo", icon=ft.Icons.WIDGETS),
            ft.NavigationDrawerDestination(label="Devolução", icon=ft.Icons.REPLAY),
            ft.NavigationDrawerDestination(label="Relatório", icon=ft.Icons.DOWNLOAD),
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
        title=ft.Text(f"Resultados para: {termo_busca}", size=22, color=ft.Colors.WHITE),
        bgcolor="#b551c7",
        actions=[
            ft.Container(
                width=40,
                height=40,
                bgcolor="white",
                border_radius=50,
                ink=True,
                margin=ft.Margin(0, 0, 10, 0),
                content=ft.Icon(
                    ft.Icons.ARROW_BACK,
                    color="#b551c7",
                    size=30
                ),
                on_click=lambda _: page.controls.clear()  # volta limpando a tela
            )
        ]
    )

    view_resultados = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment="center",
        spacing=25,
        controls=[
            ft.Container(
                height=250,
                width=800,
                image=ft.DecorationImage(
                    src="resultado_pesquisa.gif",
                    fit=ft.ImageFit.COVER
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
                        shadow=ft.BoxShadow(
                            blur_radius=20,
                            spread_radius=5,
                            color="#ffffff",
                        ),
                        content=ft.Column(
                            expand=True,
                            spacing=25,
                            horizontal_alignment="center",
                            controls=[grid]
                        )
                    )
                ]
            ),
        ]
    )

    page.controls.clear()
    page.add(view_resultados)
    page.update()