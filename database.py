# database.py
import sqlite3

# Nome do arquivo do banco de dados SQLite
DB_NAME = 'database.db'

# Função para inicializar o banco de dados e criar as tabelas se não existirem
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Cria a tabela "owners" se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS owners (
            own_id INTEGER PRIMARY KEY AUTOINCREMENT,
            own_uid TEXT UNIQUE NOT NULL,
            own_display_name TEXT,
            own_email TEXT UNIQUE NOT NULL,
            own_photo_url TEXT,
            own_created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            own_last_login_at TEXT DEFAULT CURRENT_TIMESTAMP,
            own_status TEXT NOT NULL DEFAULT 'ON' CHECK (own_status IN ('ON', 'OFF', 'DEL')),
            own_metadata TEXT
        )
    ''')

    # Cria a tabela "pads" se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pads (
            pad_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pad_created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            pad_title TEXT NOT NULL,
            pad_content TEXT,
            pad_owner INTEGER,
            pad_status TEXT NOT NULL DEFAULT 'ON' CHECK (pad_status IN ('ON', 'OFF', 'DEL')),
            pad_metadata TEXT,
            FOREIGN KEY (pad_owner) REFERENCES owners (own_id)
        )
    ''')

    conn.commit()
    conn.close()