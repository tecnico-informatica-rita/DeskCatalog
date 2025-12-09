import flet as ft
from model.model_deskcatalog import Emprestimo
from controller.controller import ControllerDeskCatalog
 
 
class emprestimo_view:
    def __init__(self, conn):
        self.controller = ControllerDeskCatalog(conn)
 
    def main(self, page: ft.Page):
        page.title = "Empréstimo"
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
 
        #Ajuda ------------------------------------------------------------------------------------------------------------
        def fechar_snack():
            snack_bar.open = False
            page.update()
 
        snack_bar = ft.SnackBar(
            content=ft.Text(" Dica de uso: Selecione um produto disponível, informe a quantidade e registre o empréstimo para o usuário desejado."),
            action="OK",
            on_action=lambda _: fechar_snack(),
            duration=9000,
        )
        page.overlay.append(snack_bar)
 
        def abrir_ajuda(e):
            snack_bar.open = True
            page.update()
 
        #Início Menu ---------------------------------------------------------------------------------------------------------------
        page.drawer = ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination("Empréstimo", icon=ft.Icons.WIDGETS),
                ft.NavigationDrawerDestination("Cadastrar Item", icon=ft.Icons.ADD_CIRCLE),
                ft.NavigationDrawerDestination("Devolução", icon=ft.Icons.REPLAY),
                ft.NavigationDrawerDestination("Ajustar Empréstimo", icon=ft.Icons.SETTINGS_OUTLINED),
                ft.NavigationDrawerDestination("Imprimir Relatório", icon=ft.Icons.DOWNLOAD),
                ft.NavigationDrawerDestination("Início", icon=ft.Icons.HOME)
            ]
        )
 
        #Barra de Menu ------------------------------------------------------------------------------------------------------------
        page.appbar = ft.AppBar(
            leading=ft.Container(
                width=50,
                height=50,
                bgcolor="#b551c7",
                border_radius=50,
                content=ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.MENU,
                            icon_size=30,
                            icon_color="white",
                            on_click=lambda _: page.open(page.drawer),
                        )
                    ],
                    alignment="center",
                    vertical_alignment="center",
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
                    ink=True,
                    margin=ft.Margin(0, 0, 20, 0),
                    on_click=abrir_ajuda,
                    content=ft.Icon(
                        ft.Icons.QUESTION_MARK,
                        color="#b551c7",
                        size=30,
                    ),
                )
            ],
        )
 
        layout = self.pagina_emprestimo(self.controller, page)
        page.add(layout)
 
 
    def pagina_emprestimo(self, controller, page):
       
        #Dados ------------------------------------------------------------------------------------------------------------
        nomes_existentes = controller.gerenciador_produto.buscar_nomes_produtos_existentes()
        produtos_disponiveis = controller.gerenciador_produto.exibir_prod_disponiveis()
 
        #Campos para inserir texto ------------------------------------------------------------------------------------------------------------
        search_input = ft.TextField(label="Buscar Produto", width=300)
        autocomplete = ft.Column()
        combo_categoria = ft.Dropdown(
            label="Categoria",
            width=200,
            disabled=True,
            options=[ft.dropdown.Option("")]
        )
        campo_qtd = ft.TextField(
            label="Quantidade",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        campo_nome = ft.TextField(label="Nome do Solicitador", width=300)
        campo_data = ft.TextField(
            label="Data de Devolução",
            width=200,
            read_only=True,
        )
        datepicker_devolucao = ft.DatePicker(
            value=None,
            on_change=lambda e: setattr(campo_data, "value", datepicker_devolucao.value.strftime("%d/%m/%Y")) or campo_data.update()
        )
 
        #Função do Calendário ------------------------------------------------------------------------------------------------------------
        def abrir_calendario(e):
            datepicker_devolucao.open = True
            page.update()
        campo_data.on_click = abrir_calendario
        page.overlay.append(datepicker_devolucao)
 
        #Tabela ------------------------------------------------------------------------------------------------------------      
        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Quantidade total")),
                ft.DataColumn(ft.Text("Quantidade de disponíveis")),
            ],
            rows=[]
        )
 
        #Funções ------------------------------------------------------------------------------------------------------------      
        def atualizar_autocomplete(e):
            texto = search_input.value.strip().title()
            autocomplete.controls.clear()
            if texto:
                sugestoes = [n for n in nomes_existentes if texto in n]
                for s in sugestoes:
                    autocomplete.controls.append(ft.TextButton(text=s, on_click=lambda x, v=s: selecionar_sugestao(v)))
            page.update()
 
        search_input.on_change = atualizar_autocomplete
 
        def selecionar_sugestao(valor):
            search_input.value = valor
            autocomplete.controls.clear()
            for p in produtos_disponiveis:
                if p["nome"] == valor:
                    combo_categoria.options = [ft.dropdown.Option(p["categoria"])]
                    combo_categoria.value = p["categoria"]
                    break
            combo_categoria.update()
            page.update()
 
        def carregar_tabela():
            tabela.rows.clear()
            for p in controller.gerenciador_produto.exibir_prod_disponiveis():
                tabela.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(p["categoria"])),
                    ft.DataCell(ft.Text(p["nome"])),
                    ft.DataCell(ft.Text(p["total_produtos"])),
                    ft.DataCell(ft.Text(p["total_disponiveis"])),
                ]))
            page.update()
 
        def snack(msg, cor):
            sb = ft.SnackBar(ft.Text(msg), bgcolor=cor)
            page.overlay.append(sb)
            sb.open = True
            page.update()
 
        def limpar_campos():
            search_input.value = ""
            campo_qtd.value = ""
            campo_nome.value = ""
            campo_data.value = ""
            combo_categoria.value = ""
            datepicker_devolucao.value = None
            page.update()
 
        def finalizar_emprestimo(emprestimo, qtd, pat):
            resposta = controller.fazer_emprestimo(emprestimo, qtd, pat)
            if resposta["status"] == "sucesso":
                snack(f"✅ Empréstimo registrado: {resposta['qtd_registrada']} item(s)", "green")
                limpar_campos()
                carregar_tabela()
            else:
                snack("⚠ Erro ao realizar empréstimo", "red")
 
        def realizar_emprestimo(e):
            try:
                nome_produto = search_input.value.strip().title()
                categoria = combo_categoria.value
                qtd = campo_qtd.value
                nome_solicitador = campo_nome.value.strip()
                data_devolucao = datepicker_devolucao.value
 
                emprestimo = Emprestimo(nome_emprestimo=nome_solicitador, data_devolucao=data_devolucao)
                resposta = controller.confimacao_usuario(emprestimo, nome_produto, categoria, qtd)
 
                if resposta["status"] == "ok":
                    return finalizar_emprestimo(emprestimo, resposta["qtd"], resposta["pat"])
                if resposta["status"] == "zerado":
                    return snack("⚠ Produto indisponível no estoque!", "red")
                if resposta["status"] == "insuficiente":
                    qtd_disp = resposta["qtd"]
                    pat = resposta["pat"]
 
                    def on_cancel(e):
                        dialogo.open = False
                        page.update()
 
                    def on_confirm(e):
                        dialogo.open = False
                        page.update()
                        finalizar_emprestimo(emprestimo, qtd_disp, pat)
 
                    dialogo = ft.AlertDialog(
                        title=ft.Text("Quantidade insuficiente"),
                        content=ft.Text(f"A quantidade solicitada não está disponível.\nDisponível: {qtd_disp} item(s).\nDeseja emprestar assim mesmo?"),
                        actions=[ft.TextButton("Cancelar", on_click=on_cancel),
                                ft.TextButton("Confirmar", on_click=on_confirm)],
                        modal=True
                    )
                    dialogo.open = True
                    page.overlay.append(dialogo)
                    page.update()
            except Exception as e:
                snack(f"❌ Erro: {e}", "red")
 
        #Estilização da Página ------------------------------------------------------------------------------------------------------------
        layout_principal = ft.Container(
            expand=True,
            bgcolor="#ffffff",
            padding=0,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment="center",
                spacing=25,
                controls=[
                    ft.Container(
                        expand=True,
                        height=250,
                        image=ft.DecorationImage(
                            src="img/emprestimo.gif",
                            fit=ft.ImageFit.COVER,
                        ),
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=800,
                                bgcolor="white",
                                border_radius=40,
                                padding=40,
                                shadow=ft.BoxShadow(
                                    blur_radius=20,
                                    spread_radius=5,
                                    color="#cccccc",
                                ),
                                content=ft.Column(
                                    expand=True,
                                    spacing=25,
                                    horizontal_alignment="center",
                                    controls=[
                                        ft.Row(
                                            [search_input, combo_categoria],
                                            alignment="center",
                                            spacing=20
                                        ),
                                        autocomplete,
                                        ft.Row(
                                            [campo_qtd, campo_nome, campo_data],
                                            alignment="center",
                                            spacing=20
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.center,
                                            content=ft.ElevatedButton(
                                                "Emprestar",
                                                color=ft.Colors.WHITE,
                                                bgcolor="#7ec151",
                                                height=50,
                                                width=300,
                                                on_click= realizar_emprestimo,
                                            ),
                                        ),
                                        ft.Divider(),
                                        ft.Text("📋 Produtos Registrados", size=22),
                                        tabela,
                                    ]
                                ),
                            )
                        ]
                    ),
                ]
            )
        )
 
        carregar_tabela()
        return layout_principal
 
#Abrir página ------------------------------------------------------------------------------------------------------------
def main(page: ft.Page):
    view = emprestimo_view()
    view.main(page)
 
ft.app(target=main)