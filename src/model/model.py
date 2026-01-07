# model.py
"""
Camada Model (Modelo):
- Define as classes de entidade (Filme).
- Define as classes de acesso a dados (GerenciadorFilmes).
- Define a lógica de negócios e cálculos (GerenciadorLanchonete, Calculos).
"""
from database.database import get_db_connection
import psycopg2
import smtplib
from email.mime.text import MIMEText
from password_validator import PasswordValidator
from config.config import servidor_smtp, porta, usuario, senha

#===== MODEL ========
def enviar_email(destinatario):
    try:
        servidor = smtplib.SMTP(servidor_smtp, porta)
        servidor.starttls()  
        servidor.login(usuario, senha)

        assunto = 'Bem vindo ao Deskcatalog!'
        corpo = 'As meninas superpoderosas ficaram muito feliz com o seu loguin! Aproveite o app :)'
        mensagem = MIMEText(corpo)
        mensagem['Subject'] = assunto
        mensagem['From'] = usuario
        mensagem['To'] = destinatario


        servidor.send_message(mensagem)
        servidor.quit()
        return True
    except:
        return False

def Autenticar_senha(senha):
    #Retorna True se uma senha tem 8 caracteres, letras e numeros
    schema = PasswordValidator()
    schema.min(8).has().letters().has().digits()
    return schema.validate(senha)

#print(Autenticar_senha('Anaclara6600'))
#print(enviar_email('anaclaragamair15@gmail.com'))

#FUNÇÃO PARA REUNIR INFORMAÇOES POR CATEGORIA NO BANCO
def pegar_linhas_da_view_do_banco(nome_view):
    """Essa função retorna a visao de determinada categoria"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {nome_view}")
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except psycopg2.OperationalError as e:
        return("Um erro inesperado aconteceu: {e}")


def separar_o_retorno_por_variavel(lista):
    """Pega a lista do banco e transforma em dicionário."""
    try:
        produtos = []
        for nome, status, unidades in lista:
            produtos.append({
                "Produto": nome,
                "Status": status,
                "Unidades": unidades
            })
        
        return produtos  
        
    except Exception as e:
        return f"Um erro inesperado aconteceu: {e}"

def separar_o_retorno_por_variavel_relatorio_30_dias(lista):
    """
    Pega a lista do banco e transforma em uma lista de dicionários
    com as colunas da view 'visao_itens_para_devolucao_30_dias'
    """
    try:
        resultado = []
        for nome_produto, nome_pessoa, id_disponibilidade, data, quantidade, status in lista:
            resultado.append({
                "Produto": nome_produto,
                "Pessoa": nome_pessoa,
                "ID_Disponibilidade": id_disponibilidade,
                "Data_Emprestimo": data,
                "Quantidade": quantidade,
                "Status": status
            })
        return resultado

    except Exception as e:
        return f"Um erro inesperado aconteceu: {e}"
    
def separar_o_retorno_por_variavel_historico_de_transaces(lista):
    """
    Pega a lista do banco e transforma em uma lista de dicionários
    com as colunas da view 'visao_historico_transacoes_emprestimos'
    """
    try:
        historico = []
        for nome_produto, nome_emprestimos, data_emprestimo, descricao_disponibilidade, quantidade_total in lista:
            historico.append({
                "Produto": nome_produto,
                "Emprestado_por": nome_emprestimos,
                "Data_emprestimo": data_emprestimo,
                "Status": descricao_disponibilidade,
                "Quantidade_total": quantidade_total
            })
        return historico
    except Exception as e:
        return f"Um erro inesperado aconteceu: {e}"

