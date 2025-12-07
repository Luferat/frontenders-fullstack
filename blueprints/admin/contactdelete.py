# blueprints\admin\contactdelete.py
# Apaga contato pelo id

import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for

from database import DB_NAME

admin_contact_delete_bp = Blueprint('admin_contact_delete', __name__,)


@admin_contact_delete_bp.route("/admin/contact/delete/<int:cid>")
def admin_contact_delete_page(cid):

    owner_uid = request.cookies.get('owner_uid').strip()

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT own_is_admin FROM owners WHERE own_uid = ? AND own_status = 'ON'", (owner_uid,))
    row = cursor.fetchone()

    if row is None or row['own_is_admin'] == 'False':
        conn.close()
        return redirect(url_for('home.home_page'))

    cursor.execute(
        "UPDATE contacts SET cnt_status = 'Apagado' WHERE cnt_id = ? AND cnt_status != 'Apagado'",
        (cid,)
    )
    conn.commit()
    conn.close()

    flash("Contato apagado com sucesso!", "success")
    return redirect(url_for('admin_contacts.admin_contacts_page'))
