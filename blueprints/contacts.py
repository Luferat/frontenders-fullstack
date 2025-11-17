# blueprints\contacts.py
# Página de contato

from flask import Blueprint, render_template

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route("/contacts")
def contacts_page():
    return render_template("contacts.html")