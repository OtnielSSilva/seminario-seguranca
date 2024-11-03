import os
from dotenv import load_dotenv
import bcrypt


def get_secret_key():
    load_dotenv()
    secret_key = os.environ["SECRET_KEY"]  # Obtém a chave secreta
    if not secret_key:
        raise EnvironmentError(
            "SECRET_KEY não definida nas variáveis de ambiente")
    return secret_key


def hash_password(password):
    # Concatena a senha com a chave secreta antes de gerar o hash
    secret_key = get_secret_key()
    password_with_secret = (password + secret_key).encode('utf-8')
    salt = bcrypt.gensalt()  # Gera um salt automaticamente
    hashed = bcrypt.hashpw(password_with_secret, salt)
    # Retorna como string para fácil armazenamento
    return hashed.decode('utf-8')


def verify_password(stored_password_hash, provided_password):
    secret_key = get_secret_key()
    password_with_secret = (provided_password + secret_key).encode('utf-8')
    return bcrypt.checkpw(password_with_secret, stored_password_hash.encode('utf-8'))
