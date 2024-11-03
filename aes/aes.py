import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Função para encriptar uma mensagem usando AES


def aes_encriptar(mensagem, chave):
    iv = get_random_bytes(AES.block_size)  # Gera um IV aleatório
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    mensagem_padded = pad(mensagem.encode("utf-8"), AES.block_size)
    mensagem_encriptada = cipher.encrypt(mensagem_padded)
    return base64.b64encode(iv + mensagem_encriptada).decode('utf-8')

# Função para decriptar uma mensagem encriptada usando AES


def aes_decriptar(mensagem_encriptada, chave):
    mensagem_encriptada = base64.b64decode(mensagem_encriptada)
    iv = mensagem_encriptada[:AES.block_size]
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    mensagem_padded = cipher.decrypt(mensagem_encriptada[AES.block_size:])
    mensagem = unpad(mensagem_padded, AES.block_size)
    return mensagem.decode("utf-8")

# Exemplo de uso


def main():
    chave = get_random_bytes(16)  # Gera uma chave de 16 bytes
    mensagem = input("Digite a mensagem para encriptar: ")

    # Encripta a mensagem
    mensagem_encriptada = aes_encriptar(mensagem, chave)
    print(f"Mensagem encriptada (Base64): {mensagem_encriptada}")

    # Decripta a mensagem
    mensagem_decriptada = aes_decriptar(mensagem_encriptada, chave)
    print(f"Mensagem decriptada: {mensagem_decriptada}")


if __name__ == "__main__":
    main()
