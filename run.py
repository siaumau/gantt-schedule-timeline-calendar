import os
import sys
import webbrowser
import subprocess
from threading import Timer
import argparse
import appdirs
import shutil

# 設定應用程序的數據目錄
APP_NAME = "ProjectManager"
APP_AUTHOR = "YourCompany"
DATA_DIR = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)

def get_resource_path(relative_path):
    """獲取資源文件的絕對路徑"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 創建臨時文件夾，將路徑存儲在 _MEIPASS 中
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def ensure_data_dir():
    """確保數據目錄存在，並返回資料庫路徑"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    db_path = os.path.join(DATA_DIR, 'gantt.db')
    
    # 如果資料庫不存在，複製 schema.sql 到數據目錄
    schema_path = get_resource_path('schema.sql')
    if not os.path.exists(db_path) and os.path.exists(schema_path):
        target_schema = os.path.join(DATA_DIR, 'schema.sql')
        shutil.copy2(schema_path, target_schema)
    
    return db_path

def backup_database(db_path):
    """備份資料庫"""
    if os.path.exists(db_path):
        backup_dir = os.path.join(DATA_DIR, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'gantt_backup_{timestamp}.db')
        
        shutil.copy2(db_path, backup_path)
        print(f'資料庫已備份至: {backup_path}')

def open_browser(port):
    webbrowser.open(f'http://127.0.0.1:{port}')

if __name__ == '__main__':
    # 添加命令行參數解析
    parser = argparse.ArgumentParser(description='專案管理系統')
    parser.add_argument('--port', type=int, default=5000, help='指定端口號（默認：5000）')
    parser.add_argument('--backup', action='store_true', help='備份當前資料庫')
    args = parser.parse_args()

    # 設置資料庫路徑
    db_path = ensure_data_dir()
    os.environ['DATABASE_PATH'] = db_path

    # 如果指定了備份參數
    if args.backup:
        backup_database(db_path)
        print(f'資料庫位置: {db_path}')
        print(f'數據目錄: {DATA_DIR}')
        exit(0)

    # 檢查資料庫
    if not os.path.exists(db_path):
        import init_db
        init_db.init_db()
    
    # 設定延遲2秒後打開瀏覽器
    Timer(2, open_browser, args=[args.port]).start()
    
    # 啟動 Flask 應用
    from app import app
    app.run(host='0.0.0.0', port=args.port) 