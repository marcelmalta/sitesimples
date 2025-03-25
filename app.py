from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os

app = Flask(__name__)

# Configuração de sessões
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "memory"
Session(app)

# Usuário e senha fixos (pra simplificar)
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "123456"

@app.route("/")
def index():
    # Verifica se o usuário está logado
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return "<h1>Bem-vindo ao meu site simples!</h1><br><a href='/logout'>Sair</a>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USUARIO_CORRETO and password == SENHA_CORRETA:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Usuário ou senha incorretos")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)