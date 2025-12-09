# view.py
"""
Camada View:
- Contém todas as funções responsáveis pela interação com o usuário.
- Funções de exibição e de obtenção de dados.
"""
import flet as ft
from model.model_deskcatalog import Produto
from controller.controller import ControllerDeskCatalog
 
 
class cadastro_view:
    def __init__(self, conn):
        self.controller = ControllerDeskCatalog(conn)
 
    def main_cadastro(self, page: ft.Page):
        page.title = "Cadastro"
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
 
        #Ajuda ------------------------------------------------------------------------------------------------------------
        def fechar_snack():
            snack_bar.open = False
            page.update()
 
        snack_bar = ft.SnackBar(
            content=ft.Text("Dica de uso: Utilize o campo 'Buscar Produto' ou cadastre novos itens, e veja-os na tabela abaixo."),
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
                ft.NavigationDrawerDestination("Cadastrar Item", icon=ft.Icons.ADD_CIRCLE),
                ft.NavigationDrawerDestination("Empréstimo", icon=ft.Icons.WIDGETS),
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
 
        layout = self.montar_layout_estilizado(self.controller, page)
        #page.add(layout)
        return layout # retornou o layout para a main
 
    def montar_layout_estilizado(self, controller, page):
 
        #Dados ------------------------------------------------------------------------------------------------------------
        categorias = controller.gerenciador_produto.buscar_nome_categorias()
        status_lista = controller.gerenciador_produto.buscar_status()
        nomes_existentes = controller.gerenciador_produto.buscar_nomes_produtos_existentes()
 
        #Campos para inserir texto ------------------------------------------------------------------------------------------------------------
        search_input = ft.TextField(label="Buscar Produto", width=300)
        autocomplete = ft.Column()
        nome_produto = ft.TextField(
            label="Nome do Produto (caso não exista no catálogo)", width=300, visible=False
        )
 
        combo_categoria = ft.Dropdown(
            label="Categoria",
            width=200,
            options=[ft.dropdown.Option(x) for x in categorias],
        )
 
        combo_status = ft.Dropdown(
            label="Status",
            width=200,
            options=[ft.dropdown.Option(x) for x in status_lista],
        )
 
        campo_qtd = ft.TextField(
            label="Quantidade",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER
        )
 
        #Tabela ------------------------------------------------------------------------------------------------------------
        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Total")),
                ft.DataColumn(ft.Text("Ativos")),
            ],
            rows=[]
        )
 
        #Funções ------------------------------------------------------------------------------------------------------------
        def atualizar_autocomplete(e):
            texto = search_input.value.strip().title()
            autocomplete.controls.clear()
 
            if texto != "":
                sugestoes = [n for n in nomes_existentes if texto in n]
                for s in sugestoes:
                    autocomplete.controls.append(
                        ft.TextButton(text=s, on_click=lambda x, v=s: selecionar_sugestao(v))
                    )
 
            nome_produto.visible = (texto != "" and texto not in nomes_existentes)
            page.update()
 
        def selecionar_sugestao(valor):
            search_input.value = valor
            nome_produto.visible = False
            autocomplete.controls.clear()
            page.update()
 
        def carregar_tabela():
            tabela.rows.clear()
            dados = controller.exibir_todosP_qtd()
 
            for item in dados:
                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item["categoria"])),
                            ft.DataCell(ft.Text(item["nome"])),
                            ft.DataCell(ft.Text(str(item["total_produtos"]))),
                            ft.DataCell(ft.Text(str(item["total_ativo"]))),
                        ]
                    )
                )
            page.update()
 
        def cadastrar_produto(e):
            try:
                nome = nome_produto.value if nome_produto.visible else search_input.value
 
                prod = Produto(
                    nome=nome,
                    categoria=combo_categoria.value,
                    quantidade=campo_qtd.value,
                    status=combo_status.value
                )
 
                resposta = controller.adicionar_produto(prod)
 
                if prod.nome not in nomes_existentes:
                    nomes_existentes.append(prod.nome)
 
                carregar_tabela()
 
                '''snackbar = ft.SnackBar(
                    ft.Text(resposta["mensagem"]),
                    bgcolor="green" if resposta["status"] == "ok" else "red"
                )'''
                # Dessa forma apareceu todos os erros na tela

                if resposta["status"] == "ok":
                    snackbar = ft.SnackBar(ft.Text(resposta["mensagem"]), bgcolor="green")
                elif resposta["status"] == 'erro':
                    snackbar = ft.SnackBar(ft.Text(resposta["mensagem"]), bgcolor="red")

                page.overlay.append(snackbar)
                snackbar.open = True

            except ValueError as erro:
                if hasattr(erro, "args") and erro.args:
                    if isinstance(erro.args[0], dict):
                        texto = erro.args[0].get("mensagem", "Erro inesperado")
                    else:
                        texto = str(erro)
                else:
                    texto = str(erro)

                snackbar = ft.SnackBar(ft.Text(f"⚠ {texto}"), bgcolor="red")
                page.overlay.append(snackbar)
                snackbar.open = True
 
            finally:
                '''search_input.value = ""
                nome_produto.value = ""
                campo_qtd.value = ""
                combo_categoria.value = None
                combo_status.value = None
                nome_produto.visible = False
                autocomplete.controls.clear()
                page.update()'''

                # Para testar se limpava nome e categoria, mas não funcionou
                # ====== LIMPAR CAMPOS ======
                nome_produto.value = ""
                search_input.value = ""
                campo_qtd.value = ""

            # Limpa os Dropdowns
                combo_categoria.value = None
                combo_status.value = None
                combo_categoria.update()
                combo_status.update()

                nome_produto.visible = False  
                autocomplete.controls.clear()
                page.update()
 
        search_input.on_change = atualizar_autocomplete
 
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
                            src="img/cadastro.gif",
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
                                        search_input,
                                        autocomplete,
                                        ft.Row(
                                            [combo_categoria, combo_status, campo_qtd],
                                            alignment="center",
                                            spacing=20
                                        ),
                                        nome_produto,
 
                                        ft.Container(
                                            alignment=ft.alignment.center,
                                            content=ft.ElevatedButton(
                                                "Cadastrar",
                                                color=ft.Colors.WHITE,
                                                bgcolor="#7ec151",
                                                height=50,
                                                width=300,
                                                on_click=cadastrar_produto,
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
'''def main(page: ft.Page): ========== Comentei pq o meu eu rodei pelo main
    view = cadastro_view(conn)
    view.main(page)
 
ft.app(target=main)'''