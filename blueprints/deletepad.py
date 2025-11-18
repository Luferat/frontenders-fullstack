# blueprints/deletepad.py
# Apaga o pad solicitado, marcando-o com status=DEL (soft delete)

import sqlite3
from flask import Blueprint, redirect, request, flash, url_for

from database import DB_NAME

delete_bp = Blueprint('delete', __name__)

@delete_bp.route("/delete/<int:pad_id>")
def deletepad(pad_id):

    # Lê o cookie 'owner_uid' (assumindo autenticação via Firebase/cookie)
    owner_uid = request.cookies.get('owner_uid')
    if not owner_uid:
        flash('Você precisa estar logado para deletar um pad.', 'error')
        return redirect(url_for('viewpad.viewpad', pad_id=pad_id))  # Assumindo blueprint 'view' para /view/<pad_id>

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Verifica se o usuário logado existe e está ativo
    cursor.execute(
        "SELECT own_uid FROM owners WHERE own_uid = ? AND own_status = 'ON'",
        (owner_uid,)
    )
    row = cursor.fetchone()

    if row and owner_uid == row['own_uid']:
        # Executa o soft delete só se o pad pertence ao owner
        cursor.execute(
            "UPDATE pads SET pad_status = 'DEL' WHERE pad_id = ? AND pad_owner = ?",
            (pad_id, owner_uid,)
        )
        if cursor.rowcount > 0:  # Verifica se atualizou algo
            conn.commit()
            flash('Pad deletado com sucesso!', 'success')
            return redirect(url_for('home.home_page'))  # Assumindo blueprint 'home' para /
        else:
            conn.commit()  # Commit mesmo em falha (opcional)
            flash('Pad não encontrado ou você não é o proprietário.', 'error')
            return redirect(url_for('viewpad.viewpad', pad_id=pad_id))
    else:
        flash('Usuário inválido ou inativo.', 'error')
        return redirect(url_for('viewpad.viewpad', pad_id=pad_id))