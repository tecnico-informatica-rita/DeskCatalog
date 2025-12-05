# código para teste da função empréstimo

import flet as ft
from controller.controller import ControllerEmprestimo
# Assumindo que você importou seu Controller e o objeto Emprestimo
# from seu_modulo_controller import ControllerEmprestimo 
# from seu_modulo_classes import Emprestimo 
# from seu_modulo_db import MockDBConnection # Use sua conexão real

# --- 1. FUNÇÕES DE INTERFACE (CHAMADAS PELO CONTROLLER) ---

def pedir_confirmacao_emprestimo_parcial_flet(page, qtd_disponivel, qtd_original):
    """
    Função que cria e exibe um AlertDialog para pedir a confirmação.
    Retorna o resultado da confirmação de volta ao Controller.
    """
    
    # Objeto que armazenará a resposta do usuário (True/False)
    user_response = [None] 

    def close_dialog(e):
        """Fecha o diálogo e atualiza a página."""
        page.dialog.open = False
        page.update()

    def handle_response(e, response):
        """Define a resposta do usuário e fecha o diálogo."""
        user_response[0] = response
        close_dialog(e)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("⚠️ Atenção: Estoque Insuficiente"),
        content=ft.Text(
            f"Você solicitou {qtd_original} itens, mas apenas {qtd_disponivel} estão disponíveis.\n"
            "Deseja prosseguir com o empréstimo parcial de APENAS estes itens?"
        ),
        actions=[
            ft.TextButton(
                "Sim, Emprestar Parcialmente",
                on_click=lambda e: handle_response(e, True)
            ),
            ft.TextButton(
                "Não, Cancelar",
                on_click=lambda e: handle_response(e, False)
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: handle_response(e, False) # Trata o fechamento pelo Esc
    )

    page.dialog = dialog
    dialog.open = True
    page.update()
    
    # Loop de espera (Bloqueia até que o usuário responda)
    while user_response[0] is None:
        # Flet é assíncrono, mas em um handler síncrono,
        # precisamos esperar a resposta (em um ambiente real, 
        # isso seria feito com Futures ou Threading, mas para 
        # a demo Flet, um loop de espera síncrono é comum em handlers).
        pass 
        
    return user_response[0]


# --- 2. CLASSE DA INTERFACE FLET (A VIEW) ---

class EmprestimoView(ft.View):
    def __init__(self, page: ft.Page, controller):
        
        # --- 1. Inicializa Elementos de Interface PRIMEIRO (CORREÇÃO) ---
        self.page = page
        self.controller = controller
        
        # Elementos de interface (DEFINIDOS AQUI)
        self.txt_nome = ft.TextField(label="Nome do Produto")
        self.txt_categoria = ft.TextField(label="Categoria")
        self.txt_qtd = ft.TextField(label="Quantidade", keyboard_type=ft.KeyboardType.NUMBER)
        self.lbl_mensagem = ft.Text("") # Rótulo para mensagens de status
        
        # --- 2. Chama super().__init__ DEPOIS ---
        super().__init__(
            route="/emprestimo",
            controls=[
                ft.AppBar(title=ft.Text("Novo Empréstimo")),
                # Agora, create_form pode acessar os atributos com segurança.
                ft.Container(content=self.create_form(page, controller), padding=20) 
            ]
        )
        
        # O self.page e self.controller já foram definidos,
        # então as linhas que estavam abaixo da chamada super()
        # devem ser removidas ou reorganizadas conforme acima.

    def create_form(self, page, controller):
        """Cria os campos e o botão da interface."""
        
        return ft.Column(
            [
                ft.Text("Dados do Produto:", weight=ft.FontWeight.BOLD),
                self.txt_nome,
                self.txt_categoria,
                self.txt_qtd,
                ft.Divider(),
                ft.ElevatedButton(
                    text="Registrar Empréstimo", 
                    on_click=self.handle_registrar
                ),
                self.lbl_mensagem,
            ]
        )

    def handle_registrar(self, e):
        """
        Handler do botão. Captura dados e chama o Controller.
        """
        self.lbl_mensagem.value = "Processando..."
        self.page.update()

        try:
            # 1. Capturar e validar entrada local
            qtd = int(self.txt_qtd.value)
            nome = self.txt_nome.value.strip()
            categoria = self.txt_categoria.value.strip()
            
            # (SIMULAÇÃO: Crie seu objeto Emprestimo real aqui)
            emprestimo_mock = type('MockEmprestimo', (object,), {'validar': lambda self: None, 
                                                                 'agora': lambda self: 'data_agora',
                                                                 'converter_data_timestamp': lambda self: 'data_devolucao_timestamp',
                                                                 'nome_emprestimo': 'Cliente Flet'})()

            # 2. Chamar o Controller
            resultado = self.controller.fazer_emprestimo(
                emprestimo_mock, 
                nome, 
                categoria, 
                qtd,
                # Passa a função Flet como callback
                callback_confirmacao=lambda qd, qo: pedir_confirmacao_emprestimo_parcial_flet(self.page, qd, qo)
            )

            # 3. Tratar e exibir o resultado
            status = resultado.get("status")
            if status == "sucesso":
                self.lbl_mensagem.value = f"✅ Sucesso! {resultado.get('qtd_registrada')} item(s) emprestado(s)."
                self.lbl_mensagem.color = ft.colors.GREEN_700
            elif status == "cancelado":
                self.lbl_mensagem.value = f"❌ Cancelado: {resultado.get('mensagem')}"
                self.lbl_mensagem.color = ft.colors.AMBER_700
            else:
                self.lbl_mensagem.value = f"🚨 ERRO: {resultado.get('mensagem', 'Falha desconhecida.')}"
                self.lbl_mensagem.color = ft.colors.RED_700

        except ValueError as ex:
            self.lbl_mensagem.value = f"🚨 ERRO DE ENTRADA/DB: {ex}"
            self.lbl_mensagem.color = ft.colors.RED_700
        except Exception as ex:
            self.lbl_mensagem.value = f"🚨 ERRO INESPERADO: {ex}"
            self.lbl_mensagem.color = ft.colors.RED_700
            
        self.page.update()


# --- 3. FUNÇÃO PRINCIPAL FLET ---

def main(page: ft.Page):
    page.title = "Gerenciador de Empréstimos (Flet)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # SIMULAÇÃO: Inicialize sua conexão e seu Controller real aqui
    conn_mock = 'sua_conexao_db' 
    controller = ControllerEmprestimo(conn_mock)
    
    # Adiciona a View à página
    page.add(EmprestimoView(page, controller))

# Para executar, use:
ft.app(target=main)