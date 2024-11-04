import tkinter as tk
from tkinter import ttk
import random

def executar_scan():
    alvo = entrada_alvo.get()
    porta = entrada_porta.get()
    tipo_scan = tipo_scan_var.get()
    resultado_text.delete(1.0, tk.END)

    if not alvo:
        resultado_text.insert(tk.END, "Por favor, insira um alvo válido.\n")
        return

    if not porta.isdigit() or not (1 <= int(porta) <= 65535):
        resultado_text.insert(tk.END, "Por favor, insira uma porta válida (1-65535).\n")
        return

    porta = int(porta)
    resultado_text.insert(tk.END, f"Iniciando {tipo_scan} em {alvo} na porta {porta}...\n\n")

    # Randomizar estado da porta
    estado = random.choice(['aberta', 'fechada', 'filtrada'])
    servico = servicos_comuns.get(porta, 'Desconhecido')

    if tipo_scan == "TCP Connect Scan":
        tcp_connect_scan(alvo, porta, estado, servico)
    elif tipo_scan == "SYN Scan":
        syn_scan(alvo, porta, estado, servico)
    elif tipo_scan == "UDP Scan":
        udp_scan(alvo, porta, estado, servico)
    else:
        resultado_text.insert(tk.END, "Tipo de scan não reconhecido.\n")

def tcp_connect_scan(alvo, porta, estado, servico):
    # Simulação do TCP Connect Scan
    resultado_text.insert(tk.END, f"Realizando conexão completa com {alvo} na porta {porta}...\n")
    if estado == 'aberta':
        resultado_text.insert(tk.END, "Three-way handshake completado (SYN, SYN-ACK, ACK).\n")
        resultado_text.insert(tk.END, f"Porta {porta}/TCP aberta. Serviço: {servico}\n")
    elif estado == 'filtrada':
        resultado_text.insert(tk.END, "Não foi possível completar o handshake.\n")
        resultado_text.insert(tk.END, f"Porta {porta}/TCP filtrada.\n")
    else:
        resultado_text.insert(tk.END, "Conexão recusada.\n")
        resultado_text.insert(tk.END, f"Porta {porta}/TCP fechada.\n")
    resultado_text.insert(tk.END, "TCP Connect Scan concluído.\n")

def syn_scan(alvo, porta, estado, servico):
    # Simulação do SYN Scan
    resultado_text.insert(tk.END, f"Enviando pacote SYN para {alvo} na porta {porta}...\n")
    if estado == 'aberta':
        resultado_text.insert(tk.END, "Recebido SYN-ACK.\n")
        resultado_text.insert(tk.END, f"Porta {porta}/TCP aberta. Serviço: {servico}\n")
    elif estado == 'filtrada':
        resultado_text.insert(tk.END, "Nenhuma resposta recebida (possível filtragem).\n")
        resultado_text.insert(tk.END, f"Porta {porta}/TCP filtrada.\n")
    else:
        resultado_text.insert(tk.END, "Recebido RST (reset).\n")
        resultado_text.insert(tk.END, f"Porta {porta}/TCP fechada.\n")
    resultado_text.insert(tk.END, "SYN Scan concluído.\n")

def udp_scan(alvo, porta, estado, servico):
    # Simulação do UDP Scan
    resultado_text.insert(tk.END, f"Enviando pacote UDP para {alvo} na porta {porta}...\n")
    if estado == 'aberta':
        resultado_text.insert(tk.END, f"Resposta recebida da porta {porta}.\n")
        resultado_text.insert(tk.END, f"Porta {porta}/UDP aberta. Serviço: {servico}\n")
    elif estado == 'filtrada':
        resultado_text.insert(tk.END, "Nenhuma resposta recebida (possível filtragem).\n")
        resultado_text.insert(tk.END, f"Porta {porta}/UDP filtrada.\n")
    else:
        resultado_text.insert(tk.END, "Recebido ICMP Port Unreachable.\n")
        resultado_text.insert(tk.END, f"Porta {porta}/UDP fechada.\n")
    resultado_text.insert(tk.END, "UDP Scan concluído.\n")

# Dicionário de serviços comuns
servicos_comuns = {
    20: 'FTP Data',
    21: 'FTP Control',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    123: 'NTP',
    135: 'RPC',
    139: 'NetBIOS',
    143: 'IMAP',
    161: 'SNMP',
    389: 'LDAP',
    443: 'HTTPS',
    445: 'SMB',
    587: 'SMTP (SSL)',
    3389: 'RDP',
    8080: 'HTTP Proxy',
    # Adicione mais portas e serviços conforme necessário
}

# Janela principal
janela = tk.Tk()
janela.title("Simulador de Scans de Rede")

# Configuração da janela
janela.geometry("500x600")
janela.resizable(False, False)

# Entrada do Alvo
label_alvo = ttk.Label(janela, text="Insira o Alvo (IP ou Domínio):")
label_alvo.pack(pady=5)
entrada_alvo = ttk.Entry(janela, width=40)
entrada_alvo.pack()

# Entrada da Porta
label_porta = ttk.Label(janela, text="Insira a Porta (1-65535):")
label_porta.pack(pady=5)
entrada_porta = ttk.Entry(janela, width=40)
entrada_porta.pack()
entrada_porta.insert(0, "80")  # Porta padrão

# Seleção do Tipo de Scan
tipo_scan_var = tk.StringVar(value="TCP Connect Scan")
label_tipo_scan = ttk.Label(janela, text="Selecione o Tipo de Scan:")
label_tipo_scan.pack(pady=5)

tipos_scan = ["TCP Connect Scan", "SYN Scan", "UDP Scan"]
combo_tipo_scan = ttk.Combobox(janela, values=tipos_scan, textvariable=tipo_scan_var, state="readonly")
combo_tipo_scan.pack()

# Botão para Executar o Scan
botao_executar = ttk.Button(janela, text="Executar Scan", command=executar_scan)
botao_executar.pack(pady=10)

# Área de Resultados
resultado_text = tk.Text(janela, height=20, width=60)
resultado_text.pack(pady=10)

# Iniciar o Loop da Interface Gráfica
janela.mainloop()
