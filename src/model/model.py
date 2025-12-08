# model.py
"""
Camada Model (Modelo):
- Define as classes de entidade (Filme).
- Define as classes de acesso a dados (GerenciadorFilmes).
- Define a lógica de negócios e cálculos (GerenciadorLanchonete, Calculos).
"""
from src.database.database import get_db_connection
import psycopg2
import smtplib
from email.mime.text import MIMEText
from password_validator import PasswordValidator
from src.config.loguin_config import servidor_smtp, porta, usuario, senha
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
    except psycopg2.Error as e:
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
