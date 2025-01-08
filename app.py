from flask import Flask, session, g, render_template, redirect, url_for, jsonify, request
from auth import auth
from db import get_db, init_app
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
# 從環境變量獲取密鑰，如果沒有則生成一個隨機密鑰
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY') or os.urandom(24)

# 初始化資料庫
init_app(app)

# 註冊認證藍圖
app.register_blueprint(auth, url_prefix='/auth')

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

@app.route('/')
def index():
    if g.user is None:
        return render_template('login.html')
    return redirect(url_for('gantt'))

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/gantt')
def gantt():
    if g.user is None:
        return redirect(url_for('login_page'))
    return render_template('gantt.html')

# 添加獲取任務數據的API路由
@app.route('/api/tasks')
def get_tasks():
    if g.user is None:
        return jsonify({'error': '請先登入'}), 401
    
    db = get_db()
    tasks = db.execute(
        'SELECT t.*, u.username FROM tasks t LEFT JOIN users u ON t.user_id = u.id'
    ).fetchall()
    return jsonify([dict(task) for task in tasks])

@app.route('/api/users')
def get_users():
    if g.user is None or g.user['username'] != 'admin':
        return jsonify({'error': '權限不足'}), 403
    
    db = get_db()
    users = db.execute('SELECT id, username, created_at FROM users').fetchall()
    return jsonify([dict(user) for user in users])

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if g.user is None or g.user['username'] != 'admin':
        return jsonify({'error': '權限不足'}), 403
    
    if user_id == g.user['id']:
        return jsonify({'error': '不能刪除自己'}), 400
    
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    return jsonify({'message': '用戶已刪除'})

@app.route('/api/users/<int:user_id>/reset-password', methods=['POST'])
def reset_password(user_id):
    if g.user is None or g.user['username'] != 'admin':
        return jsonify({'error': '權限不足'}), 403
    
    db = get_db()
    db.execute(
        'UPDATE users SET password = ? WHERE id = ?',
        (generate_password_hash('123456'), user_id)
    )
    db.commit()
    return jsonify({'message': '密碼已重置為：123456'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if g.user is None:
        return jsonify({'error': '請先登入'}), 401
    
    db = get_db()
    task = db.execute('SELECT user_id FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if task is None:
        return jsonify({'error': '任務不存在'}), 404
    
    if g.user['username'] != 'admin' and task['user_id'] != g.user['id']:
        return jsonify({'error': '權限不足'}), 403
    
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    return jsonify({'message': '任務已刪除'})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if g.user is None:
        return jsonify({'error': '請先登入'}), 401
    
    data = request.get_json()
    required_fields = ['title', 'start_date', 'end_date', 'user_id']
    
    # 檢查必要欄位
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必要欄位'}), 400
    
    try:
        db = get_db()
        db.execute(
            'INSERT INTO tasks (title, start_date, end_date, user_id) VALUES (?, ?, ?, ?)',
            (data['title'], data['start_date'], data['end_date'], data['user_id'])
        )
        db.commit()
        return jsonify({'message': '專案創建成功'}), 201
    except Exception as e:
        return jsonify({'error': f'保存失敗: {str(e)}'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if g.user is None:
        return jsonify({'error': '請先登入'}), 401
    
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if task is None:
        return jsonify({'error': '任務不存在'}), 404
    
    # 檢查權限
    if g.user['username'] != 'admin' and task['user_id'] != g.user['id']:
        return jsonify({'error': '權限不足'}), 403
    
    data = request.get_json()
    required_fields = ['title', 'start_date', 'end_date', 'user_id']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必要欄位'}), 400
    
    # 驗證日期格式
    try:
        from datetime import datetime
        datetime.strptime(data['start_date'], '%Y-%m-%d')
        datetime.strptime(data['end_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': '日期格式不正確，請使用 YYYY-MM-DD 格式'}), 400
    
    try:
        db.execute(
            'UPDATE tasks SET title = ?, start_date = ?, end_date = ?, user_id = ?, progress = ? WHERE id = ?',
            (data['title'], data['start_date'], data['end_date'], data['user_id'], data.get('progress', 0), task_id)
        )
        db.commit()
        return jsonify({'message': '專案更新成功'})
    except Exception as e:
        return jsonify({'error': f'更新失敗: {str(e)}'}), 500

@app.route('/api/users/change-password', methods=['POST'])
def change_password():
    if g.user is None:
        return jsonify({'error': '請先登入'}), 401
    
    data = request.get_json()
    if not all(k in data for k in ['old_password', 'new_password']):
        return jsonify({'error': '缺少必要欄位'}), 400
    
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (g.user['id'],)).fetchone()
    
    from werkzeug.security import check_password_hash, generate_password_hash
    
    if not check_password_hash(user['password'], data['old_password']):
        return jsonify({'error': '原密碼不正確'}), 400
    
    try:
        db.execute(
            'UPDATE users SET password = ? WHERE id = ?',
            (generate_password_hash(data['new_password']), g.user['id'])
        )
        db.commit()
        return jsonify({'message': '密碼修改成功'})
    except Exception as e:
        return jsonify({'error': f'密碼修改失敗: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    ) 