from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
import os
import random
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

# Lista de frases aleatórias
frases = [
    "Hoje é um ótimo dia para aprender algo novo!",
    "A vida é uma aventura, aproveite cada momento!",
    "Sorria, o mundo fica mais bonito assim!",
    "Você é mais forte do que imagina!",
    "O sucesso vem com dedicação e paciência."
]

# Usuário e senha fixos (pra simplificar)
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "123456"

# Variável global pra armazenar a frase atual
frase_atual = random.choice(frases)

def gerar_imagem(frase):
    largura, altura = 600, 200
    imagem = Image.new("RGB", (largura, altura), color="#2A2A2A")  # Fundo escuro
    draw = ImageDraw.Draw(imagem)
    try:
        fonte = ImageFont.truetype("arial.ttf", 24)
    except:
        fonte = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), frase, font=fonte)
    text_largura = bbox[2] - bbox[0]
    text_altura = bbox[3] - bbox[1]
    x = (largura - text_largura) / 2
    y = (altura - text_altura) / 2
    draw.text((x, y), frase, font=fonte, fill="#FFFFFF")  # Texto branco
    buffer = io.BytesIO()
    imagem.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

@app.route("/")
def index():
    # Verifica se o usuário está logado (via cookie)
    if request.cookies.get("logged_in") != "true":
        return redirect(url_for("login"))
    global frase_atual
    frase_atual = random.choice(frases)  # Escolhe uma nova frase
    return render_template("index.html", frase=frase_atual)

@app.route("/imagem")
def imagem():
    buffer = gerar_imagem(frase_atual)
    return send_file(buffer, mimetype="image/png")

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