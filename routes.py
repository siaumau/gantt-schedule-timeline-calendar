from flask import g, jsonify
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return jsonify({'error': '請先登入'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    db = get_db()
    tasks = db.execute(
        'SELECT t.*, u.username FROM tasks t LEFT JOIN users u ON t.user_id = u.id'
    ).fetchall()
    return jsonify([dict(task) for task in tasks])

@app.route('/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    # ... 驗證數據
    db = get_db()
    db.execute(
        'INSERT INTO tasks (title, start_date, end_date, user_id) VALUES (?, ?, ?, ?)',
        (data['title'], data['start_date'], data['end_date'], g.user['id'])
    )
    db.commit()
    return jsonify({'message': '任務創建成功'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if task['user_id'] != g.user['id']:
        return jsonify({'error': '您沒有權限修改此任務'}), 403
        
    data = request.get_json()
    db.execute(
        'UPDATE tasks SET title = ?, start_date = ?, end_date = ? WHERE id = ?',
        (data['title'], data['start_date'], data['end_date'], task_id)
    )
    db.commit()
    return jsonify({'message': '任務更新成功'}) 