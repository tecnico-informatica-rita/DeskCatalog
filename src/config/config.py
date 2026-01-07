# Bibliotecas necessárias ------------------------------------------------------------------------------------------------------
import os
from dotenv import load_dotenv

# Gerando conexão com banco de dados -------------------------------------------------------------------------------------------
load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DB_CONFIG = {
    'host': DB_HOST,
    'user': DB_USER,
    'port': DB_PORT,
    'password': DB_PASSWORD,
    'database': DB_NAME
}


# Gerando conexão com servidor SMTP --------------------------------------------------------------------------------------------
servidor_smtp = os.getenv("SMTP_SERVIDOR")
porta = int(os.getenv("SMTP_PORTA"))
usuario = os.getenv("SMTP_USUARIO")
senha = os.getenv("SMTP_SENHA")


    