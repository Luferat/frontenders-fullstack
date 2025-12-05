# blueprints\admin\contact.py
# Visualiza contato pelo id

import sqlite3
from flask import Blueprint, redirect, render_template, request, url_for

from database import DB_NAME

admin_contact_bp = Blueprint('admin_contact', __name__,)


@admin_contact_bp.route("/admin/contact/<int:cid>")
def admin_contact_page(cid):

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
        SELECT * 
        FROM contacts 
        WHERE cnt_status != 'Apagado'
            AND cnt_id = ?
        ORDER BY cnt_created_at DESC
    """, (cid,))
    row = cursor.fetchone()

    if row is None:
        return redirect(url_for('admin_contacts.admin_contacts_page'))
    
    cursor.execute("UPDATE contacts SET cnt_status = 'Lido' WHERE cnt_id = ? AND cnt_status != 'Apagado'", (cid,))
    conn.commit()
    conn.close()

    return render_template("admin/contact.html", contact=row)
