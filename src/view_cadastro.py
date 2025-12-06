# código para teste da função cadastro

import flet as ft
#from controller.controller import ControllerDeskCatalog
from model.model_deskcatalog import Produto

def pagina_produtos(controller, page):

    # ----- BUSCAS INICIAIS -----
    categorias = controller.gerenciador_produto.buscar_nome_categorias()
    status_lista = controller.gerenciador_produto.buscar_status()
    nomes_existentes = controller.gerenciador_produto.buscar_nomes_produtos_existentes()

    # ========== COMPONENTES ==========

    # Campos:
    search_input = ft.TextField(label="Buscar Produto", width=300, on_change=lambda e: atualizar_autocomplete(e))
    autocomplete = ft.Column()  # aparecerá a lista de sugestões
    nome_produto = ft.TextField(label="Nome do Produto (caso não exista no catálogo)", width=300, visible=False)
    combo_categoria = ft.Dropdown(label="Categoria", width=200,
                                  options=[ft.dropdown.Option(x) for x in categorias])
    combo_status = ft.Dropdown(label="Status", width=200,
                               options=[ft.dropdown.Option(x) for x in status_lista])
    campo_qtd = ft.TextField(label="Quantidade", width=150, keyboard_type=ft.KeyboardType.NUMBER)

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

        # Verifica se mostra campo de novo produto
        nome_produto.visible = (texto != "" and texto not in nomes_existentes)

        page.update()

    def selecionar_sugestao(valor):
        search_input.value = valor
        nome_produto.visible = False
        autocomplete.controls.clear()
        page.update()

    def carregar_tabela(e=None):
        tabela.rows.clear()
        dados = controller.exibir_todosP_qtd()

        for item in dados:
            tabela.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item['categoria']))),
                    ft.DataCell(ft.Text(item['nome'])),
                    ft.DataCell(ft.Text(item['total_produtos'])),
                    ft.DataCell(ft.Text(item['total_ativo'])),
                ])
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

            print("🛠 Produto criado na view:", prod.__dict__)

        # mensagem agora é um dicionário {"status": "...", "msg": "..."}
            resposta = controller.adicionar_produto(prod)

        # Se for novo nome, adiciona na lista usada pelo autocomplete
            if prod.nome not in nomes_existentes:
                nomes_existentes.append(prod.nome)

            carregar_tabela()

        # ====== MOSTRAR SNACKBAR ======
            if resposta["status"] == "ok":
                snackbar = ft.SnackBar(ft.Text(resposta["mensagem"]), bgcolor="green")
            elif resposta["status"] == 'erro':
                snackbar = ft.SnackBar(ft.Text(resposta["mensagem"]), bgcolor="red")

            page.overlay.append(snackbar)
            snackbar.open = True

            '''# ====== LIMPAR CAMPOS ======
            nome_produto.value = ""
            search_input.value = ""
            campo_qtd.value = ""
            combo_categoria.value = None
            combo_status.value = None
            nome_produto.visible = False  
            autocomplete.controls.clear()'''
           

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


    # ========== LAYOUT ==========

    layout_principal = ft.Column([
        ft.Text("📦 Catálogo de Produtos", size=20, weight=ft.FontWeight.BOLD),
        search_input,
        autocomplete,
        ft.Row([combo_categoria, combo_status, campo_qtd]),
        nome_produto,
        ft.ElevatedButton("Cadastrar", on_click=cadastrar_produto),
        ft.Divider(),
        ft.Text("📋 Produtos Registrados", size=18),
        tabela
    ])

    carregar_tabela()
    return layout_principal
