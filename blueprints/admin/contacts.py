# blueprints\admin\contacts.py
# Lista todos os contatos

import sqlite3
from flask import Blueprint, redirect, render_template, request, url_for

from database import DB_NAME

admin_contacts_bp = Blueprint('admin_contacts', __name__,)

@admin_contacts_bp.route("/admin/contacts", methods=["GET", "POST"])
def admin_contacts_page():

    owner_uid = request.cookies.get('owner_uid').strip()

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT own_isadmin FROM owners WHERE own_uid = ? AND own_status = 'ON'", (owner_uid,))
    row = cursor.fetchone()

    if row is None or row['own_isadmin'] == 'False':
        conn.close()
        return redirect(url_for('home.home_page'))

    cursor.execute("""
        SELECT cnt_id, cnt_created_at, cnt_name, cnt_email, cnt_subject, cnt_status
        FROM contacts 
        WHERE cnt_status != 'Apagado'
        ORDER BY cnt_created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return render_template("admin/contacts.html", contacts=rows)
