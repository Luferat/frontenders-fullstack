# blueprints\ownerdata.py
# Exibe detalhes do owner, principalmente todos os seus Pads

import sqlite3
from flask import Blueprint, render_template
from database import DB_NAME

# Cria o objeto blueprint da rota
ownerdata_bp = Blueprint('ownerdata', __name__)


@ownerdata_bp.route("/owner/<uid>")
def ownerdata_page(uid):

    uid = uid.strip()

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            own_id, own_uid, own_display_name, own_photo_url, own_created_at
        FROM owners
            WHERE own_uid = ?
    """, (uid,))
    own = cursor.fetchone()

    cursor.execute("""
        SELECT 
            pad_id, pad_created_at, pad_title, pad_views, 
            SUBSTR(pad_content, 1, 80) || '...' AS pad_content_preview
        FROM pads
            WHERE pad_owner = ? AND pad_status = 'ON'
        ORDER BY pad_created_at DESC;
    """, (uid,))

    pads = cursor.fetchall()
    total = len(pads)

    return render_template("owner.html", own=own, pads=pads, total=total)
