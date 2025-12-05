# blueprints\edit.py
# Edita um único registro (pad)

import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for
from database import DB_NAME

# Cria a "blueprint"
edit_bp = Blueprint('edit', __name__)


@edit_bp.route("/edit/<int:pad_id>", methods=["GET", "POST"])
def edit_page(pad_id):

    # Recebe o cookie do usuário
    owner_uid = request.cookies.get('owner_uid')
    if owner_uid is None:
        # Se  usuário não está logado, redireciona para a "home"
        return redirect(url_for('home.home_page'))

    # Conexão com o BD
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query SQL que obtém o registro a ser editado
    cursor.execute('''
        SELECT pad_id, pad_title, pad_content, pad_owner FROM pads
        WHERE pad_id = ? AND pad_status = 'ON'
    ''', (pad_id,))

    # Recebe os dados e armazena em "row"
    row = cursor.fetchone()

    # Se o registro não existe ou status != 'ON'
    if row is None:
        # Fecha o banco de dados
        conn.close()
        # Redireciona para a "home"
        return redirect(url_for('home.home_page'))

    # Se o usuário NÃO É "owner" do registro
    if row['pad_owner'] != owner_uid:
        conn.close()
        return redirect(url_for('home.home_page'))

    # Se o formulário foi enviado
    if request.method == "POST":

        # Recebe os dados preenchidos
        new_title = request.form.get("padtitle", "").strip()
        new_content = request.form.get("padcontent", "").strip()

        # Executa a query que atualiza o registro
        cursor.execute(
            'UPDATE pads SET pad_title = ?, pad_content = ? WHERE pad_id = ?',
            (new_title, new_content, pad_id,)
        )

        # Salva e fecha a conexão com o BD
        conn.commit()
        conn.close()

        # Mensgem flash enviada para a "view"
        flash("Alterações salvas com sucesso!", "success")
        return redirect(url_for("view.view_page", pad_id=pad_id))

    # Fecha conexão com DB
    conn.close()
    # Mostra formulário preenchido
    return render_template("edit.html", pad=row)
