import flet as ft
from mock_model import Emprestimo

def pagina_emprestimo(controller, page):

    nomes_existentes = controller.gerenciador_produto.buscar_nomes_produtos_existentes()
    produtos_disponiveis = controller.gerenciador_produto.exibir_prod_disponiveis()

    search_input = ft.TextField(label="Buscar Produto", width=300)
    autocomplete = ft.Column()
    combo_categoria = ft.TextField(label="Categoria", width=200, disabled=True)
    campo_qtd = ft.TextField(label="Quantidade", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    campo_nome = ft.TextField(label="Nome do Solicitador", width=300)
    campo_data = ft.TextField(label="Data de Devolução", width=200, read_only=True)
    datepicker_devolucao = ft.DatePicker(value=None)

    def abrir_calendario(e):
        datepicker_devolucao.open = True
        page.update()
    campo_data.on_click = abrir_calendario
    page.overlay.append(datepicker_devolucao)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Categoria")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Quantidade total")),
            ft.DataColumn(ft.Text("Quantidade de disponíveis")),
        ],
        rows=[]
    )

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
                page.dialog = dialogo
                dialogo.open = True
                page.update()
        except Exception as e:
            snack(f"❌ Erro: {e}", "red")

    layout = ft.Column([
        ft.Text("📦 Empréstimo de Produtos", size=20, weight=ft.FontWeight.BOLD),
        search_input,
        autocomplete,
        ft.Row([combo_categoria, campo_qtd, campo_nome, campo_data]),
        ft.ElevatedButton("Emprestar", on_click=realizar_emprestimo),
        ft.Divider(),
        ft.Text("📋 Produtos Disponíveis", size=18),
        tabela
    ])

    carregar_tabela()
    return layout