# app.py
import sqlite3
from flask import Flask, render_template
from database import DB_NAME, init_db
from owner import owner_bp
from sqlite3 import Row

app = Flask(__name__)

# Inicializa o banco de dados ao iniciar o aplicativo
init_db()

# Registra o blueprint para as rotas de owner
app.register_blueprint(owner_bp, url_prefix='/owner')

# Rota da página inicial


@app.route("/")
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
            pad_id, pad_created_at, pad_title,
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

@app.route("/contacts")
def contacts_page():
    return render_template("contacts.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/newpad")
def newpad_page():
    return render_template("newpad.html")


@app.route("/privacy")
def privacy_page():
    return render_template("privacy.html")


@app.route("/search")
def search_page():
    return render_template("search.html")


if __name__ == '__main__':
    app.run(debug=True)
