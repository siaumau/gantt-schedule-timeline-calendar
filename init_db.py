import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    # 連接到資料庫（如果不存在會創建）
    conn = sqlite3.connect('gantt.db')
    
    # 讀取 schema.sql
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema = f.read()
    
    # 執行 SQL 命令
    conn.executescript(schema)
    
    # 添加預設用戶
    default_user = {
        'username': 'admin',
        'password': generate_password_hash('admin123')
    }
    
    try:
        conn.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (default_user['username'], default_user['password'])
        )
        conn.commit()
        print("預設用戶創建成功！")
        print("預設帳號：admin")
        print("預設密碼：admin123")
    except sqlite3.IntegrityError:
        print("預設用戶已存在")
    
    # 關閉連接
    conn.close()
    print("資料庫初始化完成！")

if __name__ == '__main__':
    init_db() 