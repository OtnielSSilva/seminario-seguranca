import os
import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup


app = Flask(__name__)
app.secret_key = "chave_secreta_para_flash"

# Define o caminho do banco de dados na pasta `instance`
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{
    os.path.join(basedir, 'instance', 'usuarios.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Modelo de dados para o usuário


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


# Garante a criação da tabela
with app.app_context():
    db.create_all()
# Rota de registro para adicionar usuários


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Usuário registrado com sucesso!", "success")
        return redirect(url_for("index"))
    return render_template("register.html")

# Rota de consulta vulnerável a SQL Injection


@app.route("/insecure_query", methods=["GET", "POST"])
def insecure_query():
    results = None
    if request.method == "POST":
        username = request.form.get("username")

        # Consulta SQL vulnerável a SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}'"
        conn = sqlite3.connect(os.path.join(
            basedir, 'instance', 'usuarios.db'))
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            flash(f"Erro na consulta: {e}", "error")
        finally:
            conn.close()

        if results:
            # Exibir os resultados da consulta
            result_text = "<br>".join(
                [f"ID: {row[0]}, Usuário: {row[1]}, Senha: {row[2]}" for row in results])
            flash(
                Markup(f"<strong>Resultados da consulta:</strong><br>{result_text}"), "info")
        else:
            flash("Nenhum usuário encontrado com o critério fornecido.", "info")

    return render_template("insecure_query.html")

# Rota para login


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Consulta o usuário no banco de dados
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuário ou senha incorretos", "error")
    return render_template("login.html")

# Rota para o painel do usuário (dashboard)


@app.route("/dashboard")
def dashboard():
    return "<h1>Bem-vindo ao dashboard do usuário!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
