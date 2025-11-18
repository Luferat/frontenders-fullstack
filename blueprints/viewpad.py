# blueprints\viewpad.py
# EXibe o pad completo

import sqlite3
from flask import Blueprint, render_template, request

from database import DB_NAME


viewpad_bp = Blueprint('view', __name__)


@viewpad_bp.route("/view/<int:pad_id>")
def viewpad(pad_id):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT pads.*, own_id, own_uid, own_display_name, own_photo_url
        FROM pads
        INNER JOIN owners ON pad_owner = own_uid
        WHERE pad_id = ? AND pad_status = 'ON';                   
    ''', (pad_id,))

    row = cursor.fetchone()

    # Lê o cookie 'owners_uid'
    owner_uid = request.cookies.get('owner_uid')

    if owner_uid == row['pad_owner']:
        # Se logado e owner do pad
        is_owner = True
    else:
        # Não logado ou não é dono
        is_owner = False

    return render_template("viewpad.html", pad=row, is_owner=is_owner)
