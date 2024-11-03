from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "chave_secreta_para_flash"  # Necessário para usar flash

# Nome de usuário e senha corretos
usuario_correto = "admin"
senha_correta = "senha123"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("username")
        senha = request.form.get("password")
        if usuario == usuario_correto and senha == senha_correta:
            return redirect(url_for("dashboard"))
        else:
            flash("Usuário ou senha incorretos", "error")  # Mensagem de erro
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return "<h1>Bem-vindo ao dashboard do usuário!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
