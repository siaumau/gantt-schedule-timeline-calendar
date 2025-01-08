import sqlite3
from werkzeug.security import generate_password_hash
import os
import appdirs

def init_db():
    # 獲取數據目錄
    APP_NAME = "ProjectManager"
    APP_AUTHOR = "YourCompany"
    DATA_DIR = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)
    db_path = os.path.join(DATA_DIR, 'gantt.db')
    schema_path = os.path.join(DATA_DIR, 'schema.sql')

    # 連接到資料庫
    conn = sqlite3.connect(db_path)
    
    # 讀取 schema.sql
    with open(schema_path, 'r', encoding='utf-8') as f:
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