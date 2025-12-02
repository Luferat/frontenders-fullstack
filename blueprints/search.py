# blueprints\search.py
# Página de pesquisa

import html
import sqlite3
from flask import Blueprint, render_template, request

from database import DB_NAME

search_bp = Blueprint('search', __name__)


@search_bp.route("/search")
def search_page():

    pad_results = []
    pad_total = 0

    query = request.args.get("q", "")
    query = " ".join(query.split())
    query = html.escape(query)

    if query != '':

        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql_query = f"%{query}%"

        cursor.execute("""
            SELECT
                pad_id, pad_created_at, pad_title, pad_owner,
                own_id, own_display_name, own_photo_url,
                SUBSTR(pad_content, 1, 50) || '...' AS pad_content_preview
            FROM pads
            INNER JOIN owners ON pad_owner = own_uid
            WHERE pad_status = 'ON' AND (
                pad_title LIKE ? OR
                pad_content LIKE ?
            )
            ORDER BY pad_created_at DESC;
        """, (sql_query, sql_query))

        rows = cursor.fetchall()
        pad_results = [dict(row) for row in rows]
        pad_total = len(pad_results)

        conn.close()

    return render_template(
        "search.html",
        query=query,
        pad_results=pad_results,
        pad_total=pad_total
    )
