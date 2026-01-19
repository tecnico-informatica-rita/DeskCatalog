import flet as ft
from model.model_deskcatalog import Emprestimo
from controller.controller import ControllerDeskCatalog

class devolucao_view:
    def __init__(self, conn):
        self.controller = ControllerDeskCatalog(conn)

    def main_devolucao(self, page: ft.Page):
        page.title = "Devolução"
        page.window.resizable = False
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0

        # ===================== AJUDA ==========================
        def fechar_snack():
            snack_bar.open = False
            page.update()

        snack_bar = ft.SnackBar(
            content=ft.Text("Dica: Selecione o produto emprestado, informe quem vai devolver e registre."),
            action="OK",
            on_action=lambda _: fechar_snack(),
            duration=9000,
        )
        page.overlay.append(snack_bar)

        def abrir_ajuda(e):
            snack_bar.open = True
            page.update()

        # ===================== MENU ==========================
        page.drawer = ft.NavigationDrawer(
            on_change=lambda e: page.go([
                "/devolucao",   
                "/cadastro",  
                "/emprestimo",   
                "/relatorio",   
                "/",           
            ][e.control.selected_index]),
            controls=[
                ft.NavigationDrawerDestination("Devolução", icon=ft.Icons.REPLAY),
                ft.NavigationDrawerDestination("Cadastrar Item", icon=ft.Icons.ADD_CIRCLE),
                ft.NavigationDrawerDestination("Empréstimo", icon=ft.Icons.WIDGETS),
                ft.NavigationDrawerDestination("Relatório", icon=ft.Icons.DOWNLOAD),
                ft.NavigationDrawerDestination("Início", icon=ft.Icons.HOME)
            ]
        )

        page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.MENU,
                icon_color="white",
                on_click=lambda _: page.open(page.drawer),
            ),
            title=ft.Text("", size=22, color=ft.Colors.WHITE),
            bgcolor="#b551c7",
            actions=[
                ft.IconButton(ft.Icons.QUESTION_MARK, icon_color="white", on_click=abrir_ajuda)
            ],
        )

        return self.pagina_devolucao(self.controller, page)

    # ===================== PÁGINA PRINCIPAL ==========================
    def pagina_devolucao(self, controller, page):
        produtos_emprestados = controller.exibir_prod_devolucao()

        search_input = ft.TextField(label="Buscar Produto", width=300)
        autocomplete = ft.Column()
        combo_categoria = ft.Dropdown(label="Categoria", width=200, disabled=True)
        campo_qtd = ft.TextField(label="Quantidade a Devolver", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        campo_nome = ft.TextField(label="Nome de quem está devolvendo", width=300)

        # ===================== TABELA ==========================
        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Item")),
                ft.DataColumn(ft.Text("Empréstimo (nome)")),
                ft.DataColumn(ft.Text("Data do empréstimo")),
                ft.DataColumn(ft.Text("Disponibilidade")),
                ft.DataColumn(ft.Text("Quantidade")),
            ],
            rows=[]
        )

        def carregar_tabela():
            tabela.rows.clear()
            for p in controller.exibir_prod_devolucao():
                tabela.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(p["produto"])),
                    ft.DataCell(ft.Text(p["nome_emprestimo"])),
                    ft.DataCell(ft.Text(p["data_emprestimo"])),
                    ft.DataCell(ft.Text(p["disponibilidade"])),
                    ft.DataCell(ft.Text(p["qtd"])),
                ]))
            page.update()

        # ===================== AUTOCOMPLETE ==========================
        def atualizar_autocomplete(e):
            texto = (search_input.value or "").strip().title()
            autocomplete.controls.clear()
            if texto:
                sugestoes = [n["produto"] for n in produtos_emprestados if texto in n["produto"].title()]
                for s in sugestoes:
                    autocomplete.controls.append(ft.TextButton(text=s, on_click=lambda x, v=s: selecionar_sugestao(v)))
            page.update()

        search_input.on_change = atualizar_autocomplete

        def selecionar_sugestao(valor):
            search_input.value = valor
            autocomplete.controls.clear()
            for p in produtos_emprestados:
                if p["produto"] == valor:
                    combo_categoria.options = [ft.dropdown.Option(p["categoria"])]
                    combo_categoria.value = p["categoria"]
                    break
            combo_categoria.update()
            page.update()

        # ===================== FEEDBACK =========================
        def snack(msg, cor):
            sb = ft.SnackBar(ft.Text(msg), bgcolor=cor)
            page.overlay.append(sb)
            sb.open = True
            page.update()

        def limpar():
            search_input.value = ""
            campo_qtd.value = ""
            campo_nome.value = ""
            combo_categoria.value = ""
            autocomplete.controls.clear()
            page.update()

        # ===================== FINALIZAR DEVOLUÇÃO ==========================
        def finalizar(emprestimo, qtd, pat):
            resposta = controller.fazer_devolucao(emprestimo, qtd, pat)
            if resposta["status"] == "sucesso":
                snack(f"📦 {resposta['qtd_registrada']} item(s) devolvido(s)!", "green")
                limpar()
                carregar_tabela()
            else:
                snack("❌ Erro ao registrar devolução!", "red")

        # ===================== BOTÃO DEVOLVER ==========================
        def devolver(e):
            try:
                nome_produto = (search_input.value or "").strip().title()
                categoria = combo_categoria.value
                qtd = campo_qtd.value
                nome_devolucao = (campo_nome.value or "").strip()

                # validações rápidas no front-end
                if not nome_produto:
                    return snack("⚠ Informe o produto a devolver.", "red")
                if not categoria:
                    return snack("⚠ Produto inválido. Selecione a sugestão correta.", "red")
                if not nome_devolucao:
                    return snack("⚠ Informe o nome de quem devolve.", "red")
                if not qtd:
                    return snack("⚠ Informe a quantidade.", "red")

                # Criar o objeto Emprestimo usando o campo que seu controller espera
                emprestimo = Emprestimo(nome_emprestimo=nome_devolucao)

                # Chamar a confirmação (uso da função existente no seu controller)
                resposta = controller.confimacao_usuario(emprestimo, nome_produto, categoria, qtd)

                if resposta["status"] == "ok":
                    return finalizar(emprestimo, resposta["qtd"], resposta["pat"])

                if resposta["status"] == "zerado":
                    return snack("❌ Nenhum item deste produto está emprestado!", "red")

                if resposta["status"] == "insuficiente":
                    qtd_disp = resposta["qtd"]
                    pat = resposta["pat"]

                    dialogo = ft.AlertDialog(
                        title=ft.Text("Quantidade Maior que o Total"),
                        content=ft.Text(f"Há apenas {qtd_disp} emprestado(s). Deseja devolver assim mesmo?"),
                        actions=[
                            ft.TextButton("Cancelar", on_click=lambda x: fechar_dialog(dialogo)),
                            ft.TextButton("Confirmar", on_click=lambda x: (fechar_dialog(dialogo), finalizar(emprestimo, qtd_disp, pat)))
                        ],
                        modal=True
                    )
                    abrir_dialog(dialogo)

            except Exception as e:
                snack(f"❌ Erro: {e}", "red")

        def abrir_dialog(d):
            d.open = True
            page.overlay.append(d)
            page.update()

        def fechar_dialog(d):
            d.open = False
            page.update()

        # ===================== LAYOUT ==========================
        layout = ft.Container(
            expand=True,
            bgcolor="white",
            padding=0,
            content=ft.Column(
                spacing=25,
                horizontal_alignment="center",
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        height=250,
                        image=ft.DecorationImage(src="img/devolucao.gif", fit=ft.ImageFit.COVER),
                    ),
                    ft.Container(
                        width=800,
                        bgcolor="white",
                        border_radius=40,
                        padding=40,
                        shadow=ft.BoxShadow(blur_radius=20, spread_radius=5, color="#cccccc"),
                        content=ft.Column(
                            spacing=25,
                            controls=[
                                ft.Row([search_input, combo_categoria], alignment="center"),
                                autocomplete,
                                ft.Row([campo_qtd, campo_nome], alignment="center"),
                                ft.ElevatedButton("Devolver", color="white", bgcolor="#7ec151", height=50, width=300, on_click=devolver),
                                ft.Divider(),
                                ft.Text("📌 Itens Emprestados", size=22),
                                tabela
                            ]
                        ),
                    )
                ]
            )
        )

        carregar_tabela()
        return layout
