# blueprints\home.py
# Processa as rotas para a página inicial do aplicativo

import sqlite3
from flask import Blueprint, render_template
from database import DB_NAME

# Cria o objeto blueprint da rota
home_bp = Blueprint('home', __name__)

@home_bp.route("/")
@home_bp.route("/home")  # Para não precisar alterar o JavaScript
def home_page():

    # Obtém todos os pads do banco de dados
    # Ordenados por `pad_created_at` mais recente
    # Somente com `status = 'ON'`

    # Conecta ao banco de dados
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Executa a consulta
    cursor.execute('''
        SELECT
            pad_id, pad_created_at, pad_title, pad_owner,
            own_id, own_display_name, own_photo_url,
            SUBSTR(pad_content, 1, 30) || '...' AS pad_content_preview
        FROM pads
        INNER JOIN owners ON pad_owner = own_id 
            WHERE pad_status = 'ON'
            ORDER BY pad_created_at DESC;
    ''')

    # Variável com os dados retornados
    rows = cursor.fetchall()
    all_pads = [dict(row) for row in rows]

    # Alguns Debugs
    # print('\n\n\n', all_pads[0][2], '\n\n\n') # Assim funciona
    # print('\n\n\n', all_pads, '\n\n\n')  # Mas quero assim

    # Passa os resultados para a página HTML
    return render_template("home.html", all_pads=all_pads)