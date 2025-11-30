# blueprints\delete.py
# Apaga o registro informado.
# Apenas marca com 'status="DEL"'

import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for

from database import DB_NAME

delete_bp = Blueprint('delete', __name__)


@delete_bp.route("/delete/<int:pad_id>")
def delete_page(pad_id):

    # Lê o cookie 'owner_uid' e verifica se está logado
    owner_uid = request.cookies.get('owner_uid')
    if owner_uid is None:
        return redirect(url_for('home.home_page'))

    # Conecta ao banco de dados
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE pads SET pad_status = 'DEL' 
        WHERE pad_id = ? AND pad_owner = ?
    ''', (pad_id, owner_uid))
    conn.commit()

    # Redireciona para a página inicial
    flash('Pad deletado com sucesso!', 'success')
    return redirect(url_for('home.home_page'))
