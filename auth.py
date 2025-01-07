from flask import Blueprint, request, jsonify, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用戶名和密碼都必須填寫'}), 400
        
    db = get_db()
    try:
        db.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
        return jsonify({'message': '註冊成功'}), 201
    except db.IntegrityError:
        return jsonify({'error': '用戶名已存在'}), 400

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    
    if user is None or not check_password_hash(user['password'], password):
        return jsonify({'error': '用戶名或密碼錯誤'}), 401
        
    session.clear()
    session['user_id'] = user['id']
    return jsonify({'message': '登入成功'}), 200

@auth.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html') 