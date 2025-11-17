# blueprints\newpad.py
# Página de cadastro de novo pad

from flask import Blueprint, render_template

newpad_bp = Blueprint('newpad', __name__)


@newpad_bp.route("/newpad")
def newpad_page():
    return render_template("newpad.html")
