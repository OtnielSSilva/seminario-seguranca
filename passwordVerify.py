import tkinter as tk
import re

def verificar_forca_senha(event):
    senha = entrada_senha.get()
    pontuacao, criterios_status = calcular_forca_senha(senha)

    if pontuacao <= 2:
        mensagem = "Senha Fraca"
        cor = "red"
    elif pontuacao == 3:
        mensagem = "Senha Média"
        cor = "orange"
    else:
        mensagem = "Senha Forte!"
        cor = "green"

    resultado_label.config(text=mensagem, fg=cor)

    # Atualizar cores dos critérios
    for i, atendido in enumerate(criterios_status):
        if atendido:
            criterio_labels[i].config(fg='green')
        else:
            criterio_labels[i].config(fg='red')

def calcular_forca_senha(senha):
    pontuacao = 0
    criterios_status = []

    # Critério 1: Comprimento da senha
    if len(senha) >= 8:
        pontuacao += 1
        criterios_status.append(True)
    else:
        criterios_status.append(False)

    # Critério 2: Letras maiúsculas e minúsculas
    if re.search(r"[A-Z]", senha) and re.search(r"[a-z]", senha):
        pontuacao += 1
        criterios_status.append(True)
    else:
        criterios_status.append(False)

    # Critério 3: Números
    if re.search(r"[0-9]", senha):
        pontuacao += 1
        criterios_status.append(True)
    else:
        criterios_status.append(False)

    # Critério 4: Caracteres especiais
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        pontuacao += 1
        criterios_status.append(True)
    else:
        criterios_status.append(False)

    # Critério 5: Evitar sequências comuns ou nomes próprios
    sequencias_comuns = ['1234', 'senha', 'password', 'abcd']
    nomes_proprios = ["gabriel", "jorge", "Otniel", "Glauber"]  
    if not any(seq in senha.lower() for seq in sequencias_comuns + nomes_proprios):
        pontuacao += 1
        criterios_status.append(True)
    else:
        criterios_status.append(False)

    return pontuacao, criterios_status

def toggle_senha():
    if entrada_senha.cget('show') == '':
        entrada_senha.config(show='*')
        botao_toggle.config(text='Mostrar')
    else:
        entrada_senha.config(show='')
        botao_toggle.config(text='Ocultar')

# Janela principal
janela = tk.Tk()
janela.title("Verificador de Força de Senha")

# Configuração da janela
janela.geometry("450x400")
janela.resizable(False, False)

# Frame para a entrada de senha e o botão
senha_frame = tk.Frame(janela)
senha_frame.pack(pady=10)

# Label de Senha
label_senha = tk.Label(senha_frame, text="Digite a senha:")
label_senha.pack(side=tk.LEFT, padx=(0, 5))

# Entrada de Senha
entrada_senha = tk.Entry(senha_frame, show="*")
entrada_senha.pack(side=tk.LEFT)
entrada_senha.bind("<KeyRelease>", verificar_forca_senha)

# Botão para Mostrar/Ocultar Senha
botao_toggle = tk.Button(senha_frame, text="Mostrar", command=toggle_senha)
botao_toggle.pack(side=tk.LEFT, padx=(5, 0))

# Label de Resultado
resultado_label = tk.Label(janela, text="", font=("Arial", 14, "bold"))
resultado_label.pack(pady=10)

# Frame para os critérios
criterios_frame = tk.Frame(janela)
criterios_frame.pack(pady=10)

# Lista de textos dos critérios
criterios_texto = [
    "• Use pelo menos 8 caracteres.",
    "• Use uma combinação de letras maiúsculas e minúsculas.",
    "• Inclua números na sua senha.",
    "• Tente inserir caracteres especiais.",
    "• Evite nomes próprios ou sequências comuns (ex: '1234')."
]

# Criação dos labels dos critérios
criterio_labels = []
for texto in criterios_texto:
    label = tk.Label(criterios_frame, text=texto, font=("Arial", 10), fg='red', anchor='w', justify='left')
    label.pack(anchor='w')
    criterio_labels.append(label)

# Iniciar o Loop da Interface Gráfica
janela.mainloop()
