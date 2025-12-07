# blueprints\search.py
# Página de pesquisa

import html
import sqlite3
from flask import Blueprint, render_template, request
from database import DB_NAME

search_bp = Blueprint('search', __name__)


@search_bp.route("/search")
def search_page():

    # Inicializa as principais variáveis
    pad_results = []
    pad_total = 0

    # Obtém o campo do formulário e sanitizar
    query = request.args.get("q", "")
    query = " ".join(query.split())
    query = html.escape(query)

    # Se solicitou uma pesquisa...
    if query != '':

        # Conecta no DB
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Prepara a pesquisa
        sql_query = f"%{query}%"

        # Query SQL de pesquisa
        cursor.execute("""
            SELECT
                pad_id, pad_created_at, pad_title, pad_owner, pad_is_markdown,
                own_id, own_display_name, own_photo_url,
                SUBSTR(pad_content, 1, 50) || '...' AS pad_content_preview
            FROM pads
            INNER JOIN owners ON pad_owner = own_uid
            WHERE pad_status = 'ON' AND (
                pad_title LIKE ? COLLATE NOCASE OR
                pad_content LIKE ? COLLATE NOCASE
            )
            ORDER BY pad_created_at DESC;
        """, (sql_query, sql_query))

        # Obtém o resultado
        rows = cursor.fetchall()
        pad_results = [dict(row) for row in rows]

        # Obtém o total de registro encontrados
        pad_total = len(pad_results)

        # Fecha o BD
        conn.close()

    # Exibe a página HTML
    return render_template(
        "search.html",
        query=query,
        pad_results=pad_results,
        pad_total=pad_total,
        page_title=f'Pesquisando por "{query}"' if query else "Pesquisar"
    )
