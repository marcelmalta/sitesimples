from flask import Flask, render_template, request, redirect, url_for, make_response
import os

app = Flask(__name__)

# Usuário e senha fixos (pra simplificar)
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "123456"

@app.route("/")
def index():
    # Verifica se o usuário está logado (via cookie)
    if request.cookies.get("logged_in") != "true":
        return redirect(url_for("login"))
    return "<h1>Bem-vindo ao meu site simples!</h1><br><a href='/logout'>Sair</a>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USUARIO_CORRETO and password == SENHA_CORRETA:
            # Cria uma resposta com um cookie
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie("logged_in", "true")
            return resp
        else:
            return render_template("login.html", error="Usuário ou senha incorretos")
    return render_template("login.html")

@app.route("/logout")
def logout():
    # Remove o cookie ao fazer logout
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("logged_in", "", expires=0)
    return resp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)