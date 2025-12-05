# database.py
import sqlite3
import os

DB_NAME = 'database.db'

add_owners = True
add_fakes = True

def init_db():
    # Conexão
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # --- Criação das tabelas ---

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            cnt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnt_created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            cnt_name TEXT,
            cnt_email TEXT,
            cnt_subject TEXT,
            cnt_message TEXT,
            cnt_status TEXT NOT NULL DEFAULT 'Recebido'
                CHECK (cnt_status IN ('Recebido','Lido','Respondido','Apagado')),
            cnt_metadata TEXT
        )
    ''')

    # --- Inserts seguros (idempotentes) ---

    if add_owners:
        cursor.executemany(
            '''
            INSERT OR IGNORE INTO owners
            (own_id, own_uid, own_display_name, own_email, own_photo_url, own_created_at, own_last_login_at, own_isadmin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            [
                ('1', 'yzfYicMZxLM34M7CfYTPQl7Pj182','André Luferat','andre@luferat.net', 'https://lh3.googleusercontent.com/a/ACg8ocKxQS94-RYr_kReF-M-1ZgXwlZBcVaDNhb9ZpQPG0le0G5WAQOD=s96-c', '2025-11-03 14:46:59','2025-12-05 15:43:56','True'),
                ('2', '50kPEJMxfhdfk0mQHn60SnTSq192','Luferat CataBits','catabits@gmail.com', 'https://lh3.googleusercontent.com/a/ACg8ocLxL_XA-Lo9mEuBsIQzhsratQ772AfEL9OzlLt7YJ9U12cQy6OB=s96-c', '2025-11-12 11:08:34','2025-12-05 15:35:27','False')
            ]
        )

    if add_fakes:
        cursor.executemany(
            '''
            INSERT OR IGNORE INTO pads
            (pad_id, pad_title, pad_content, pad_created_at, pad_status, pad_owner)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            [
                ('2', 'Receita de Bolo de Chocolate', 'Ingredientes: 2 xícaras de farinha, 1 xícara de açúcar, 3 ovos. Modo: Misture tudo e asse por 30 min. Delícia!', '2025-11-11 10:00:00', 'ON', 'yzfYicMZxLM34M7CfYTPQl7Pj182'),
                ('2', 'Dicas para Viajar Barato', 'Compre passagens com antecedência, use hostels e coma street food. Aventura garantida!', '2025-11-10 14:30:00', 'ON', '50kPEJMxfhdfk0mQHn60SnTSq192'),
                ('3', 'Como Treinar Seu Cachorro', 'Use petiscos como recompensa, treine comandos básicos como senta e fica. Paciência é chave!', '2025-11-09 09:15:00', 'ON', 'yzfYicMZxLM34M7CfYTPQl7Pj182'),
                ('4', 'Receita de Pizza Caseira', 'Massa: farinha, água, fermento. Recheio: molho, queijo, pepperoni. Asse em forno quente.', '2025-11-08 16:45:00', 'ON', '50kPEJMxfhdfk0mQHn60SnTSq192'),
                ('5', 'Melhores Filmes de Comédia', 'Recomendo "Se Beber Não Case" e "Superbad". Risadas non-stop!', '2025-11-07 11:20:00', 'ON', 'yzfYicMZxLM34M7CfYTPQl7Pj182'),
                ('6', 'Dicas de Jardinagem para Iniciantes', 'Escolha plantas resistentes, regue moderadamente e use sol adequado. Verde na casa!', '2025-11-06 13:50:00', 'ON', '50kPEJMxfhdfk0mQHn60SnTSq192'),
                ('7', 'Receita de Smoothie Energético', 'Banana, morango, iogurte e espinafre. Bata no liquidificador para um boost matinal.', '2025-11-05 08:30:00', 'ON', 'yzfYicMZxLM34M7CfYTPQl7Pj182'),
                ('8', 'Histórias Engraçadas de Viagem', 'Uma vez, confundi o trem e acabei em outra cidade. Lição: leia as placas!', '2025-11-04 15:10:00', 'ON', '50kPEJMxfhdfk0mQHn60SnTSq192'),
                ('9', 'Como Fazer Exercícios em Casa', 'Flexões, abdominais e corrida no lugar. Sem academia necessária!', '2025-11-03 17:40:00', 'ON', 'yzfYicMZxLM34M7CfYTPQl7Pj182'),
                ('10', 'Receita de Cookies Perfeitos', 'Manteiga, açúcar, farinha e gotas de chocolate. Asse até dourar. Irresistíveis!', '2025-11-02 12:00:00', 'ON', '50kPEJMxfhdfk0mQHn60SnTSq192')
            ]
        )

    conn.commit()
    conn.close()
