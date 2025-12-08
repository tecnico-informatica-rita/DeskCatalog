# view para testar as funções de empréstimo

import flet as ft

from model.model_deskcatalog import Emprestimo


def pagina_emprestimo(controller, page):

    # ----- BUSCAS INICIAIS -----
    nomes_existentes = controller.gerenciador_produto.buscar_nomes_produtos_existentes()
    produtos_disponiveis = controller.exibir_todosP_qtd()  # lista de dicts com categoria, nome, total_produtos, total_ativo

    # ========== COMPONENTES ==========
    search_input = ft.TextField(label="Buscar Produto", width=300, on_change=lambda e: atualizar_autocomplete(e))
    autocomplete = ft.Column()  # lista de sugestões
    combo_categoria = ft.TextField(label="Categoria", width=200, disabled=True)  # preenchido automaticamente
    campo_qtd = ft.TextField(label="Quantidade", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    campo_nome = ft.TextField(label="Nome do Solicitador", width=300)

    def atualizar_data(e):
        if datepicker_devolucao.value:
            campo_data.value = str(datepicker_devolucao.value)
            page.update()

    datepicker_devolucao = ft.DatePicker(
        value=None,
        on_change=atualizar_data
    )
    page.overlay.append(datepicker_devolucao)

    campo_data = ft.TextField(
        label="Data de Devolução",
        width=200,
        read_only=True,
        on_click=lambda e: abrir_calendario()
    ) 

    def abrir_calendario():
        datepicker_devolucao.open = True
        page.update()

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Categoria")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Quantidade total")),
            ft.DataColumn(ft.Text("Quantidade de ativos")),
        ],
        rows=[]
    )

    # ===== FUNÇÕES LÓGICAS =====

    def atualizar_autocomplete(e):
        texto = search_input.value.strip().title()
        autocomplete.controls.clear()

        if texto != "":
            sugestoes = [n for n in nomes_existentes if texto in n]
            for s in sugestoes:
                autocomplete.controls.append(
                    ft.TextButton(text=s, on_click=lambda x, v=s: selecionar_sugestao(v))
                )

        page.update()

    def selecionar_sugestao(valor):
        search_input.value = valor
        autocomplete.controls.clear()
        # Definir automaticamente a categoria
        categoria = None
        for prod in produtos_disponiveis:
            if prod['nome'] == valor:
                categoria = prod['categoria']
                break
        combo_categoria.value = categoria
        combo_categoria.update()
        page.update()

    def carregar_tabela(e=None):
        tabela.rows.clear()
        for item in produtos_disponiveis:
            tabela.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item['categoria']))),
                    ft.DataCell(ft.Text(item['nome'])),
                    ft.DataCell(ft.Text(item['total_produtos'])),
                    ft.DataCell(ft.Text(item['total_ativo'])),
                ])
            )
        page.update()
    
    '''def fechar_dialog(dialog):
        dialog.open = False
        page.update()

    def confirmar_dialog(dialog, emprestimo, qtd, pat_validos):
        dialog.open = False
        page.update()
        finalizar_emprestimo(emprestimo, qtd, pat_validos)

    def finalizar_emprestimo(emprestimo, qtd, pat_validos):
            resposta = controller.fazer_emprestimo(emprestimo, qtd, pat_validos)

            if resposta["status"] == "sucesso":
                snack(f"✅ Empréstimo registrado: {resposta['qtd_registrada']} item(s)", "green")
                limpar_campos()
                carregar_tabela()
            else:
                snack("⚠ Erro ao realizar empréstimo", "red")
    
    def limpar_campos():
            search_input.value = ""
            campo_qtd.value = ""
            campo_nome.value = ""
            datepicker_devolucao.value = None
            campo_data.value = ""
            combo_categoria.value = ""
            page.update()

    def snack(msg, cor):
            snackbar = ft.SnackBar(ft.Text(msg), bgcolor=cor)
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()


    def realizar_emprestimo(e):
        try:
            nome_produto = search_input.value.strip().title()
            categoria = combo_categoria.value
            qtd = (campo_qtd.value)
            nome_solicitador = campo_nome.value.strip()
            data_devolucao = datepicker_devolucao.value

        # Criar instância de Emprestimo
            emprestimo = Emprestimo(
                nome_emprestimo=nome_solicitador,
                data_devolucao=data_devolucao,
            )

        # 1️⃣ Primeiro passo → Pergunta ao controller
            resposta = controller.confimacao_usuario(emprestimo, nome_produto, categoria, qtd)

        # 2️⃣ Caso normal → segue direto
            if resposta["status"] == "ok":
                return finalizar_emprestimo(emprestimo, resposta["qtd"], resposta["pat"])

            #if resposta["status"] ==  "zerado":
                #snack(f"⚠ Produto indisponível no estoque!", "red")
        # 3️⃣ Caso insuficiente → mostrar POPUP
            if resposta["status"] == "insuficiente":
                qtd_disp = resposta["qtd"]
                pat_emprestados = resposta["pat"]
                print("Entrou no insuficiente:", resposta)
                dialogo = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Quantidade insuficiente"),
                    content=ft.Text(f"A quantidade solicitada não está disponível.\n"
                                f"Disponível: {qtd_disp} item(s).\n"
                                f"Deseja emprestar assim mesmo?"),
                    actions=[
                        ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(dialogo)),
                        ft.TextButton("Confirmar", 
                            on_click=lambda e: confirmar_dialog(dialogo, emprestimo, qtd_disp, pat_emprestados))
                    ]
                )

                page.dialog = dialogo
                dialogo.open = True
                page.update()
                return
            if resposta["status"] == "insuficiente":
                qtd_disp = resposta["qtd"]
                pat_emprestados = resposta["pat"]
                print("Entrou no insuficiente:", resposta)

                def on_cancel(e):
                    dialogo.open = False
                    page.update()

                def on_confirm(e):
                    dialogo.open = False
                    page.update()
                    confirmar_dialog(dialogo, emprestimo, qtd_disp, pat_emprestados)

                dialogo = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Quantidade insuficiente"),
                    content=ft.Text(f"A quantidade solicitada não está disponível.\n"
                            f"Disponível: {qtd_disp} item(s).\n"
                            f"Deseja emprestar assim mesmo?"),
                    actions=[
                        ft.TextButton("Cancelar", on_click=on_cancel),
                        ft.TextButton("Confirmar", on_click=on_confirm)
                    ]
                )

                page.dialog = dialogo
                dialogo.open = True
                page.update()

        except ValueError as erro:
            snack(f"⚠ {str(erro)}", "red")
        except Exception as e:
            snack(f"❌ Erro inesperado: {e}", "red")'''


    def snack(msg, cor="blue"):
        """Exibe uma mensagem rápida na tela."""
        snackbar = ft.SnackBar(ft.Text(msg), bgcolor=cor)
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()


    def limpar_campos():
        """Limpa todos os campos do formulário."""
        search_input.value = ""
        campo_qtd.value = ""
        campo_nome.value = ""
        datepicker_devolucao.value = None
        campo_data.value = ""
        combo_categoria.value = ""
        page.update()


    def finalizar_emprestimo(emprestimo, qtd, pat_validos):
        """Chama o controller para registrar o empréstimo e atualiza a interface."""
        resposta = controller.fazer_emprestimo(emprestimo, qtd, pat_validos)
        if resposta["status"] == "sucesso":
            snack(f"✅ Empréstimo registrado: {resposta['qtd_registrada']} item(s)", "green")
            limpar_campos()
            carregar_tabela()
        else:
            snack("⚠ Erro ao realizar empréstimo", "red")


    def confirmar_dialog(dialog, emprestimo, qtd, pat_validos):
        """Confirma empréstimo mesmo com quantidade menor que a solicitada."""
        dialog.open = False
        page.update()
        finalizar_emprestimo(emprestimo, qtd, pat_validos)


    def fechar_dialog(dialog):
        """Fecha o pop-up sem realizar nenhuma ação."""
        dialog.open = False
        page.update()


    '''def realizar_emprestimo(e):
        """Função principal chamada pelo botão 'Realizar Empréstimo'."""
        try:
            nome_produto = search_input.value.strip().title()
            categoria = combo_categoria.value
            qtd = campo_qtd.value
            nome_solicitador = campo_nome.value.strip()
            data_devolucao = datepicker_devolucao.value

            # Cria instância do empréstimo
            emprestimo = Emprestimo(
                nome_emprestimo=nome_solicitador,
                data_devolucao=data_devolucao,
            )

            # Pergunta ao controller se a quantidade está disponível
            try:
                resposta = controller.confimacao_usuario(emprestimo, nome_produto, categoria, qtd)
            except ValueError as erro:
            # Estoque zerado ou erro de validação
                snack(f"⚠ {str(erro)}", "red")
                return

        # Estoque suficiente → realiza empréstimo direto
            if resposta["status"] == "ok":
                return finalizar_emprestimo(emprestimo, resposta["qtd"], resposta["pat"])

        # Estoque insuficiente → mostra pop-up pedindo confirmação
            if resposta["status"] == "insuficiente":
                qtd_disp = resposta["qtd"]
                pat_emprestados = resposta["pat"]

                dialogo = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Quantidade insuficiente"),
                    content=ft.Text(
                        f"A quantidade solicitada não está disponível.\n"
                        f"Disponível: {qtd_disp} item(s).\n"
                        f"Deseja emprestar assim mesmo?"
                    ),
                    actions=[
                         ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(dialogo)),
                        ft.TextButton("Confirmar", on_click=lambda e: confirmar_dialog(dialogo, emprestimo, qtd_disp, pat_emprestados))
                    ]
                )

            # Funções de callback para o pop-up
                def on_cancel(e):
                    fechar_dialog(dialogo)

                def on_confirm(e):
                    confirmar_dialog(dialogo, emprestimo, qtd_disp, pat_emprestados)

                dialogo.actions.extend([
                    ft.TextButton("Cancelar", on_click=on_cancel),
                    ft.TextButton("Confirmar", on_click=on_confirm)
                ])

                page.dialog = dialogo
                dialogo.open = True
                page.update()

        except Exception as e:
            snack(f"❌ Erro inesperado: {e}", "red")'''
    
    def realizar_emprestimo(e):
        """Função principal chamada pelo botão 'Realizar Empréstimo'."""
        try:
            # Captura os valores dos campos
            nome_produto = search_input.value.strip().title()
            categoria = combo_categoria.value
            nome_solicitador = campo_nome.value.strip()
            data_devolucao = datepicker_devolucao.value

        # Verifica quantidade válida
            try:
                qtd_int = int(campo_qtd.value)
                if qtd_int <= 0:
                    raise ValueError("Quantidade deve ser maior que zero.")
            except ValueError:
                snack("⚠ Quantidade inválida", "red")
                return

        # Cria instância de empréstimo
            emprestimo = Emprestimo(
                nome_emprestimo=nome_solicitador,
                data_devolucao=data_devolucao,
            )

        # Pergunta ao controller se a quantidade está disponível
            try:
                resposta = controller.confimacao_usuario(emprestimo, nome_produto, categoria, qtd_int)
            except ValueError as erro:
                snack(f"⚠ {str(erro)}", "red")
                return

        # Estoque suficiente → realiza empréstimo direto
            if resposta["status"] == "ok":
                return finalizar_emprestimo(emprestimo, resposta["qtd"], resposta["pat"])

        # Estoque insuficiente → mostra pop-up pedindo confirmação
            if resposta["status"] == "insuficiente":
                qtd_disp = resposta["qtd"]
                pat_emprestados = resposta["pat"]

                dialogo = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Quantidade insuficiente"),
                    content=ft.Text(
                        f"A quantidade solicitada não está disponível.\n"
                        f"Disponível: {qtd_disp} item(s).\n"
                        f"Deseja emprestar assim mesmo?"
                    ),
                    actions=[
                        ft.TextButton(
                            "Cancelar",
                            on_click=lambda e: fechar_dialog(dialogo)
                        ),
                        ft.TextButton(
                            "Confirmar",
                            on_click=lambda e: confirmar_dialog(dialogo, emprestimo, qtd_disp, pat_emprestados)
                        )
                    ]
                )

                page.dialog = dialogo
                dialogo.open = True
                page.update()

        except Exception as e:
            snack(f"❌ Erro inesperado: {e}", "red")


    # ========== LAYOUT ==========
    layout_principal = ft.Column([
        ft.Text("📦 Empréstimo de Produtos", size=20, weight=ft.FontWeight.BOLD),
        search_input,
        autocomplete,
        ft.Row([
            combo_categoria,
            campo_qtd,
            campo_nome,
            campo_data
        ]),
        ft.ElevatedButton("Emprestar", on_click=realizar_emprestimo),
        ft.Divider(),
        ft.Text("📋 Produtos Disponíveis", size=18),
        tabela
    ])

    carregar_tabela()
    return layout_principal



