import time

def monitorar_log(arquivo_log, palavra_chave):
    with open(arquivo_log, 'r') as arquivo:
        arquivo.seek(0, 2)  # Move o cursor para o final do arquivo
        while True:
            linha = arquivo.readline()
            if not linha:
                time.sleep(1)
                continue
            if palavra_chave in linha:
                print(f"Alerta! Palavra-chave '{palavra_chave}' encontrada: {linha.strip()}")

if __name__ == "__main__":
    nome_arquivo_log = "exemplo.log"
    palavra_chave = input("Digite a palavra-chave para monitorar: ")

    # Cria um arquivo de log de exemplo
    with open(nome_arquivo_log, 'w') as arquivo:
        arquivo.write("Iniciando o log de eventos do sistema.\n")

    print(f"Monitorando o arquivo {nome_arquivo_log} em busca de '{palavra_chave}'...")
    monitorar_log(nome_arquivo_log, palavra_chave)
