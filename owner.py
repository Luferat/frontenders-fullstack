# owner.py
from flask import Blueprint, request, jsonify
from database import DB_NAME
import sqlite3

owner_bp = Blueprint('owner', __name__)

@owner_bp.route('/login', methods=['POST'])
def owner_login():
    data = request.json  # Recebe os dados do usuário em JSON

    # Validação básica dos dados recebidos (ajuste conforme necessário)
    if not data or 'uid' not in data or 'email' not in data or 'createdAt' not in data or 'lastLoginAt' not in data:
        return jsonify({'error': 'Dados inválidos'}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Verifica se o usuário já existe na tabela owners (baseado no UID do Firebase)
    cursor.execute('SELECT own_id FROM owners WHERE own_uid = ?', (data['uid'],))
    existing_user = cursor.fetchone()

    if existing_user:
        # Atualiza os dados existentes (exceto created_at, que permanece o original)
        cursor.execute('''
            UPDATE owners SET
                own_display_name = ?,
                own_email = ?,
                own_photo_url = ?,
                own_last_login_at = ?,
                own_status = 'ON'
            WHERE own_uid = ?
        ''', (data.get('displayName'), data['email'], data.get('photoURL'), data['lastLoginAt'], data['uid']))
    else:
        # Insere um novo usuário
        cursor.execute('''
            INSERT INTO owners (own_uid, own_display_name, own_email, own_photo_url, own_created_at, own_last_login_at, own_status)
            VALUES (?, ?, ?, ?, ?, ?, 'ON')
        ''', (data['uid'], data.get('displayName'), data['email'], data.get('photoURL'), data['createdAt'], data['lastLoginAt']))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Usuário persistido com sucesso'}), 200