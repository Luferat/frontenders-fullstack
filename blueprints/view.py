# blueprints\view.py
# Exibe um único registro (pad) com detalhes

from flask import Blueprint, render_template, request

view_bp = Blueprint('view', __name__)


@view_bp.route("/view/<int:pad_id>")
def search_page(pad_id):

    # Lê o cookie 'owner_uid'
    owner_uid = request.cookies.get('owner_uid')

    print('\n\n\n', pad_id, owner_uid,'\n\n\n')
    return render_template("view.html")
