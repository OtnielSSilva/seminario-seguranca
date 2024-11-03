import base64
import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class AESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Criptografia AES")
        self.root.configure(bg="#f0f2f5")
        self.chave = get_random_bytes(16)  # Gera uma chave aleatória

        # Criação dos elementos da interface
        self.create_widgets()

    def create_widgets(self):
        # Entrada da mensagem para encriptar
        tk.Label(self.root, text="Mensagem para encriptar:",
                 bg="#f0f2f5", font=("Arial", 12, "bold")).pack(pady=5)
        self.mensagem_entry = tk.Entry(self.root, width=50, font=("Arial", 10))
        self.mensagem_entry.pack(pady=5)

        # Botão para encriptar a mensagem
        tk.Button(self.root, text="Encriptar", command=self.encriptar,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

        # Label e campo de texto para mostrar a mensagem encriptada
        tk.Label(self.root, text="Mensagem encriptada (Base64):",
                 bg="#f0f2f5", font=("Arial", 12, "bold")).pack(pady=5)
        self.mensagem_encriptada_entry = tk.Entry(
            self.root, width=50, font=("Arial", 10))
        self.mensagem_encriptada_entry.pack(pady=5)

        # Botão para decriptar a mensagem encriptada
        tk.Button(self.root, text="Decriptar", command=self.decriptar,
                  bg="#007BFF", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

        # Label para a mensagem decriptada
        tk.Label(self.root, text="Mensagem decriptada:", bg="#f0f2f5",
                 font=("Arial", 12, "bold")).pack(pady=5)
        self.mensagem_decriptada_label = tk.Label(
            self.root, text="", fg="#333333", bg="#f0f2f5", font=("Arial", 10, "italic"))
        self.mensagem_decriptada_label.pack(pady=5)

    def encriptar(self):
        mensagem = self.mensagem_entry.get()
        if mensagem:
            iv = get_random_bytes(AES.block_size)  # Gera um IV aleatório
            cipher = AES.new(self.chave, AES.MODE_CBC, iv)
            mensagem_padded = pad(mensagem.encode("utf-8"), AES.block_size)
            mensagem_encriptada = cipher.encrypt(mensagem_padded)
            mensagem_encriptada_base64 = base64.b64encode(
                iv + mensagem_encriptada).decode('utf-8')
            self.mensagem_encriptada_entry.delete(0, tk.END)
            self.mensagem_encriptada_entry.insert(
                0, mensagem_encriptada_base64)
        else:
            messagebox.showwarning(
                "Aviso", "Por favor, insira uma mensagem para encriptar.")

    def decriptar(self):
        mensagem_encriptada_base64 = self.mensagem_encriptada_entry.get()
        if mensagem_encriptada_base64:
            try:
                mensagem_encriptada = base64.b64decode(
                    mensagem_encriptada_base64)
                iv = mensagem_encriptada[:AES.block_size]
                cipher = AES.new(self.chave, AES.MODE_CBC, iv)
                mensagem_padded = cipher.decrypt(
                    mensagem_encriptada[AES.block_size:])
                mensagem_decriptada = unpad(
                    mensagem_padded, AES.block_size).decode("utf-8")
                self.mensagem_decriptada_label.config(text=mensagem_decriptada)
            except (ValueError, KeyError):
                messagebox.showerror(
                    "Erro", "Falha na decriptação. Verifique se a mensagem encriptada está correta.")
        else:
            messagebox.showwarning(
                "Aviso", "Por favor, insira uma mensagem encriptada em Base64.")


# Inicializa a interface gráfica
root = tk.Tk()
app = AESApp(root)
root.mainloop()
