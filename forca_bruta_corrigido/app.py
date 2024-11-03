from flask import Flask, render_template, request, redirect, url_for, flash
import time

app = Flask(__name__)
app.secret_key = "chave_secreta_para_flash"

# Configurações de bloqueio
tentativas_maximas = 3
tempo_bloqueio = 30

# Classe de modelo de usuário


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tentativas_falhas = 0
        self.bloqueio_tempo = 0.0

    def verificar_bloqueio(self):
        if time.time() < self.bloqueio_tempo:
            return True
        return False

    def resetar_tentativas(self):
        self.tentativas_falhas = 0
        self.bloqueio_tempo = 0.0


# Cria um usuário de exemplo
usuario_correto = User("admin", "senha123")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("username")
        senha = request.form.get("password")

        # Verifica se o usuário está correto
        if usuario != usuario_correto.username:
            flash("Usuário não encontrado.", "error")
            return redirect(url_for("login"))

        # Verifica se o usuário está bloqueado
        if usuario_correto.verificar_bloqueio():
            tempo_restante = int(usuario_correto.bloqueio_tempo - time.time())
            flash(f"Usuário bloqueado. Tente novamente em {
                  tempo_restante} segundos.", "error")
            return redirect(url_for("login"))

        # Verifica as credenciais
        if usuario_correto.password == senha:
            # Limpa tentativas falhas em caso de sucesso
            usuario_correto.resetar_tentativas()
            return redirect(url_for("dashboard"))
        else:
            # Incrementa o contador de tentativas falhas
            usuario_correto.tentativas_falhas += 1
            flash("Usuário ou senha incorretos", "error")

            # Verifica se as tentativas falhas atingiram o limite
            if usuario_correto.tentativas_falhas >= tentativas_maximas:
                usuario_correto.bloqueio_tempo = time.time() + tempo_bloqueio
                flash(f"Usuário bloqueado por {
                      tempo_bloqueio} segundos devido a múltiplas tentativas.", "error")
                usuario_correto.tentativas_falhas = 0  # Reseta o contador após bloquear

            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return "<h1>Bem-vindo ao dashboard do usuário!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
