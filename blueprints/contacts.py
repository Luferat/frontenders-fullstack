# blueprints\contacts.py
# Página de contato

import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for

from database import DB_NAME

contacts_bp = Blueprint('contacts', __name__)


@contacts_bp.route("/contacts", methods=["GET", "POST"])
def contacts_page():

    # Obtém o cookie do usuário
    owner_uid = request.cookies.get('owner_uid')
    # print('\n\n\n', owner_uid, '\n\n\n')

    # Conecta com o banco de dados
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Se não está logado (não tem cookie)
    if owner_uid is None:
        # Fazer 'form.name', 'form.email' vazios
        own_name = ""
        own_email = ""
    else:
        # Recuperar os dados do BD
        cursor.execute(
            "SELECT own_display_name, own_email FROM owners WHERE own_uid = ?",
            (owner_uid,)
        )
        own = cursor.fetchone()
        # print('\n\n\n', own['own_display_name'], own['own_email'], '\n\n\n')

        # Preenche 'form.name' e 'form.email'
        own_name = own['own_display_name']
        own_email = own['own_email']

        # Atribui à variável "form" (abaixo) → form.name, form.email

    # Inicializa campos do formulário
    form = {
        "name": own_name,
        "email": own_email,
        "subject": "",
        "message": ""
    }

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

        # Salva a query no BD e fecha a conexão
        conn.commit()
        conn.close()

        # Se o contato foi salvo no BD
        if cursor.rowcount == 1:
            # Apaga dados do formulário
            form = {
                "name": own_name,
                "email": own_email,
                "subject": "",
                "message": ""
            }
            # Mensagem flash para a próxima rota
            flash("Contato enviado com sucesso!", "success")
        else:
            # Mensagem flash para a próxima rota
            flash(
                "Oooops! Não foi possível enviar o contato. Tente novamente...", "danger")

    return render_template("contacts.html", form=form)
