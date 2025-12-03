# blueprints\contacts.py
# Página de contato

import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for

from database import DB_NAME

contacts_bp = Blueprint('contacts', __name__)


@contacts_bp.route("/contacts", methods=["GET", "POST"])
def contacts_page():

    # Obtém o cookie do usuário
    # Se está logado
        # Recuperar os dados do BD
        # Atribui à variável "form" (abaixo) → form.name, form.email
    # Se não está logado
        # Fazer 'form.name', 'form.email' vazios

    # Inicializa campos do formulário
    form = {}

    # Se o form foi enviado...
    if request.method == "POST":

        # Obtém os valores dos campos e sanitiza
        form = {
            "name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "subject": request.form.get("subject", "").strip(),
            "message": request.form.get("message", "").strip(),
        }

        # Debug - Dados do form recebidos
        # print('\n\n\n', form, '\n\n\n')

        # Conecta com o banco de dados
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query de insersão usado "prepared query"
        cursor.execute("""
            INSERT INTO contacts (
                cnt_name, cnt_email, cnt_subject, cnt_message
            ) VALUES (
                ?, ?, ?, ?
            )
        """, (
            form["name"],
            form["email"],
            form["subject"],
            form["message"],
        ))

        # Salva a query no BD
        conn.commit()

        # Se o contato foi salvo no BD
        if cursor.rowcount == 1:
            # Fecha o BD
            conn.close()
            # Apaga dados do formulário
            form = {}
            # Mensagem flash para a próxima rota
            flash("Contato enviado com sucesso!", "success")
        else:
            # Fecha o BD
            conn.close()
            # Mensagem flash para a próxima rota
            flash(
                "Oooops! Não foi possível enviar o contato. Tente novamente...", "danger")

    return render_template("contacts.html", form=form)
