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
        
    view_resultados = ft.View(
            "/resultados",
            bgcolor="#ffffff",
            controls=[
                ft.AppBar(
                    title=ft.Text(f"Resultados para: {termo_busca}"),
                    bgcolor="#b551c7",
                    leading=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color="white",
                        on_click=lambda _: page.go("/")
                    ),
                ),
                ft.Container(padding=20, content=grid)
            ]
        )

    page.views.clear()
    page.views.append(view_resultados)
    page.update()