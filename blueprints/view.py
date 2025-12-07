# blueprints\view.py
# Exibe um único registro (pad) com detalhes

import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for
from database import DB_NAME
from markdown_it import MarkdownIt

view_bp = Blueprint('view', __name__)
md = MarkdownIt()


@view_bp.route("/view/<int:pad_id>")
def view_page(pad_id):

    # Lê o cookie 'owner_uid'
    owner_uid = request.cookies.get('owner_uid')

    # Conecta ao banco de dados
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # SQL de consulta com preparated query
    cursor.execute('''
        SELECT 
            pads.*, own_uid, own_display_name, own_photo_url, own_status
        FROM pads
        INNER JOIN owners ON pad_owner = own_uid
        WHERE pad_id = ? AND pad_status = 'ON'
    ''', (pad_id,))

    # Obtém o resultado da conulta
    row = cursor.fetchone()

    # Se não encontrou o pad, redireciona para a '/'
    if row is None:
        # Pad não encontrado ou foi deletado → vai pra home com mensagem
        flash('Este bloco de notas não existe ou foi removido.', 'info')
        # ajuste o nome do blueprint se necessário
        return redirect(url_for('home.home_page'))

    # Verifica se o usuário está logado e é owner do pad atual
    is_owner = (row['pad_owner'] == owner_uid)

    # Se for markdown, converte para HTML
    pad_html = None
    if row["pad_is_markdown"] == "True":
        pad_html = md.render(row["pad_content"])

    # Atualiza views do pad
    cursor.execute(
        "UPDATE pads SET pad_views = pad_views + 1 WHERE pad_id = ?", (pad_id,))
    conn.commit()
    conn.close()

    return render_template(
        "view.html",
        pad=row,
        is_owner=is_owner,
        pad_html=pad_html,
        page_title=row['pad_title']
    )
