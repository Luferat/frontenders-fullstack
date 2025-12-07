# blueprints\newpad.py
# Página de cadastro de novo pad

import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for
from database import DB_NAME

# Cria a "blueprint"
newpad_bp = Blueprint('newpad', __name__)

# Rota válida para os "method" "GET" e "POST"
@newpad_bp.route("/new", methods=["GET", "POST"])
def newpad_page():

    # Recebendo o cookie do usuário
    owner_uid = request.cookies.get('owner_uid')
    if owner_uid is None:
        # Redirecuima para a "home" se o cookie não existe
        return redirect(url_for('home.home_page'))

    # Se o formulário foi enviado, processa ele
    if request.method == "POST":

        # Recebe e filtra os valores preenchidos pelo usuário
        new_title = request.form.get("padtitle", "").strip()
        new_content = request.form.get("padcontent", "").strip()
        is_markdown = "True" if request.form.get("padmarkdown") == "True" else "False"

        # Conecta com o Banco de dados
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Faz a insersão do novo registro no banco de dados
        cursor.execute(
            """
            INSERT INTO pads (
                pad_title,
                pad_content,
                pad_is_markdown,
                pad_owner
            )
            VALUES (?, ?, ?, ?)
            """,
            (new_title, new_content, is_markdown, owner_uid)
        )

        # Executa e encerra a conexão
        conn.commit()
        conn.close()

        # Envia mensagem "flash" e redireciona para a "home"
        flash("Novo pad cadastrado!", "success")
        return redirect(url_for("home.home_page"))

    # Exibe o formulário (metodo "GET")
    return render_template("newpad.html")