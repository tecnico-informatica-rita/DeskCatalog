import flet as ft

def home_header(on_search=None):
    # ---- função interna da pesquisa ----
    def enviar_pesquisa(e):
        if on_search:
            texto = e.control.value.strip()
            if texto:
                on_search(texto)

    # ---- campo de pesquisa ----
    pesquisa = ft.TextField(
        hint_text="Pesquisa ...",
        width=500,
        border_radius=30,
        bgcolor="white",
        border_color="transparent",
        prefix_icon=ft.Icons.SEARCH,
        on_submit=enviar_pesquisa,
    )

    return ft.Stack(
        clip_behavior=ft.ClipBehavior.NONE,
        controls=[
            # ===== FUNDO COM GIF =====
            ft.Container(
                height=650,
                expand=True,
                image=ft.DecorationImage(
                    src="img/degrade_home.gif",
                    fit=ft.ImageFit.COVER
                ),
            ),

            # ===== BARRA DE PESQUISA (MESMA LÓGICA QUE VOCÊ USAVA) =====
            ft.Container(
                padding=260,  # mantido porque é o que FUNCIONA no seu layout
                alignment=ft.alignment.top_center,
                content=ft.Column(
                    [pesquisa],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                )
            ),
        ]
    )
