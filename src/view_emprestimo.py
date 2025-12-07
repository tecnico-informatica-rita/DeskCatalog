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

    def realizar_emprestimo(e):
        try:
            nome_produto = search_input.value.strip().title()
            categoria = combo_categoria.value
            qtd = (campo_qtd.value)
            nome_solicitador = campo_nome.value.strip()
            data_devolucao = datepicker_devolucao.value

            #if not nome_produto or not categoria or not nome_solicitador or not data_devolucao:
                #raise ValueError("Preencha todos os campos obrigatórios!")

            # Criar instância de Emprestimo (a classe preenche a data do empréstimo)
            emprestimo = Emprestimo(
                nome_emprestimo=nome_solicitador,
                data_devolucao=data_devolucao,
            )

            resposta = controller.fazer_emprestimo(emprestimo, nome_produto, categoria, qtd)

            if resposta["status"] == "sucesso":
                snackbar = ft.SnackBar(ft.Text(f"✅ Empréstimo realizado: {resposta['qtd_registrada']} item(s)"), bgcolor="green")
                # Limpar campos
                search_input.value = ""
                campo_qtd.value = ""
                campo_nome.value = ""
                datepicker_devolucao.value = None
                campo_data.value = "" 
                combo_categoria.value = ""
                carregar_tabela()
            else:
                snackbar = ft.SnackBar(ft.Text(f"⚠ {resposta.get('mensagem', 'Erro ao realizar empréstimo')}"), bgcolor="red")

            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()

        except ValueError as erro:
            snackbar = ft.SnackBar(ft.Text(f"⚠ {erro}"), bgcolor="red")
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()

        except Exception as e:
            snackbar = ft.SnackBar(ft.Text(f"❌ Erro inesperado: {e}"), bgcolor="red")
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()

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



