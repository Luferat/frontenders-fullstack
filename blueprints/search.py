# blueprints\search.py
# Página de pesquisa

import html
import sqlite3
from flask import Blueprint, render_template, request

from database import DB_NAME

search_bp = Blueprint('search', __name__)


@search_bp.route("/search")
def search_page():
    return render_template("search.html")
