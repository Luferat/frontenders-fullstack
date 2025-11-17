# blueprints\owner.py
# Controla a persistência do usuário
# Controla o cookie de autenticação

from flask import Blueprint, make_response, request, jsonify
from database import DB_NAME
import sqlite3

owner_bp = Blueprint('owner', __name__)


@owner_bp.route('/login', methods=['POST'])
def owner_login():
    # Recebe os dados do usuário em JSON
    data = request.json
    # print(data)  # Debug - Exibe o JSON que vem do front-end

    # Validação básica dos dados recebidos (ajuste conforme necessário)
    if not data or 'uid' not in data or 'email' not in data or 'createdAt' not in data or 'lastLoginAt' not in data:
        return jsonify({'error': 'Dados inválidos'}), 400

    # Conecta ao banco de dados
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Verifica se o usuário já existe na tabela owners (baseado no UID do Firebase)
    cursor.execute(
        'SELECT own_id FROM owners WHERE own_uid = ?', (data['uid'],))
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
        ''', (
            data.get('displayName'),
            data.get('email'),
            data.get('photoURL'),
            data.get('lastLoginAt'),
            data.get('uid')
        ))
    else:
        # Insere um novo usuário
        cursor.execute('''
            INSERT INTO owners (
                own_uid, 
                own_display_name, 
                own_email, 
                own_photo_url, 
                own_created_at, 
                own_last_login_at, 
                own_status
            ) VALUES (?, ?, ?, ?, ?, ?, 'ON')
        ''', (
            data.get('uid'),
            data.get('displayName'),
            data.get('email'),
            data.get('photoURL'),
            data.get('createdAt'),
            data.get('lastLoginAt')
        ))

    conn.commit()
    conn.close()

    # Cria a resposta JSON
    response = make_response(
        jsonify({'message': 'Usuário persistido com sucesso'}), 200)

    # Defina o tempo de vida do cookie em dias
    days_age = 10

    # Define o cookie seguro com o UID quando fizer login
    # - secure=True: Envia apenas via HTTPS (em produção; em dev, defina como False se necessário)
    # - httponly=True: Impede acesso via JavaScript (protege contra XSS)
    # - samesite='Strict': Protege contra CSRF, permitindo apenas do mesmo site
    max_age = 3600 * 24 * days_age
    response.set_cookie(
        'owner_uid',
        data['uid'],
        max_age=max_age,
        secure=True,
        httponly=True,
        samesite='Strict'
    )

    return response

# Apaga o cookie do usuário quando fizer logout
@owner_bp.route('/logout', methods=['POST'])
def owner_logout():

    # Opcional: Verifique o body se necessário, mas aqui não é estritamente preciso
    data = request.json
    if data.get('action') != 'logout':
        return jsonify({'error': 'Ação inválida'}), 400

    # Cria a resposta JSON
    response = make_response(jsonify({'message': 'Logout bem-sucedido'}), 200)
    
    # Apaga o cookie seguro
    response.delete_cookie('owner_uid')

    return response