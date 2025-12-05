# database.py
# Estrutura e controle do banco de dados
# Inicializa o banco de dados e cria as tabelas se não existirem

import sqlite3

# Nome do arquivo do banco de dados SQLite
DB_NAME = 'database.db'

add_owners = True
add_fakes = True

def init_db():
    # Cria o banco de dados, se não existe, e faz a conexão
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
            own_isadmin TEXT DEFAULT 'False',
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
            pad_views INTEGER DEFAULT 0,
            pad_owner TEXT,
            pad_status TEXT NOT NULL DEFAULT 'ON' CHECK (pad_status IN ('ON', 'OFF', 'DEL')),
            pad_metadata TEXT,
            FOREIGN KEY (pad_owner) REFERENCES owners (own_uid)
        )
    ''')

    # Cria a tabela "contacts" se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            cnt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnt_created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            cnt_name TEXT,
            cnt_email TEXT,
            cnt_subject TEXT,
            cnt_message TEXT,
            cnt_status TEXT NOT NULL DEFAULT 'Recebido' CHECK (cnt_status IN ('Recebido','Lido','Respondido','Apagado')),
            cnt_metadata TEXT
        )
    ''')

    conn.commit()
    conn.close()
