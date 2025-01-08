# 專案管理系統說明文件

## 系統簡介
基於 Flask 和 DHTMLX Gantt 開發的專案管理系統，提供甘特圖視覺化管理功能。

## 主要功能
1. 甘特圖功能
   - 拖拉調整時程
   - 切換時間尺度（日/週/月/年）
   - 顯示進度百分比

2. 專案管理
   - 新增和編輯專案
   - 設定時程
   - 分配負責人
   - 更新進度

3. 用戶管理（限管理員）
   - 用戶帳號管理
   - 密碼重置
   - 權限設定

## 快速開始

### 安裝步驟

1. 建立虛擬環境
python -m venv venv
2. 啟動虛擬環境
Windows:
venv\Scripts\activate
Linux/Mac:
source venv/bin/activate
3. 安裝套件
pip install flask
4. 初始化資料庫
python init_db.py
5. 啟動應用
python app.py

### 預設帳號
- 管理員帳號：admin
- 管理員密碼：admin123

## 系統架構
- 後端：Flask (Python)
- 前端：DHTMLX Gantt + Tailwind CSS
- 資料庫：SQLite

## 檔案說明
- `app.py`: 主程式
- `init_db.py`: 資料庫初始化
- `schema.sql`: 資料庫結構
- `templates/`: 前端模板
  - `gantt.html`: 主頁面
  - `login.html`: 登入頁
  - `logout.html`: 登出頁

## 使用須知
1. 必須先初始化資料庫
2. 修改 SECRET_KEY
3. 建議使用 Python 3.7+

## 權限說明
- 管理員：完整系統權限
- 一般用戶：僅可管理自己的專案

## 注意事項
1. 首次使用需建立資料庫
2. 請妥善保管管理員密碼
3. 定期備份資料庫檔案

## 安全配置

### SECRET_KEY 設置
1. 開發環境：
   ```bash
   # Windows
   set FLASK_SECRET_KEY=your-secret-key
   
   # Linux/Mac
   export FLASK_SECRET_KEY=your-secret-key
   ```

2. 生產環境：
   - 使用強密鑰
   - 不要在代碼中硬編碼
   - 建議使用環境變量或配置文件
   - 定期更換密鑰

### 注意事項
- 請勿將 SECRET_KEY 提交到版本控制系統
- 生產環境必須使用強密鑰
- 如果懷疑密鑰洩露，請立即更換

## 打包說明

### 1. 安裝必要套件
```bash
pip install pyinstaller appdirs
```

### 2. 執行打包
```bash
# 使用配置文件打包
pyinstaller gantt.spec
```

打包完成後，可在 `dist` 目錄下找到執行檔：
- Windows: `ProjectManager.exe`
- Linux/Mac: `ProjectManager`

### 3. 執行檔使用說明
- 直接執行：使用預設 5000 端口
  ```bash
  ProjectManager.exe
  ```

- 指定端口執行：
  ```bash
  ProjectManager.exe --port 8080
  ```

## 資料庫管理

### 1. 資料庫位置
資料庫檔案存放在用戶數據目錄：
- Windows: `C:\Users\<username>\AppData\Local\YourCompany\ProjectManager`
- Linux: `~/.local/share/ProjectManager`
- Mac: `~/Library/Application Support/ProjectManager`

### 2. 備份功能
1. 使用命令行備份：
   ```bash
   ProjectManager.exe --backup
   ```
   - 會在數據目錄下創建 `backups` 資料夾
   - 備份檔案格式：`gantt_backup_YYYYMMDD_HHMMSS.db`

2. 手動備份：
   - 直接複製 `gantt.db` 檔案
   - 建議在系統關閉時進行備份

### 3. 版本更新注意事項
1. 更新前備份資料庫
2. 資料庫位於用戶數據目錄，不會被更新覆蓋
3. 可使用 `--backup` 參數進行自動備份

## 故障排除

### 1. 找不到資料庫
- 檢查用戶數據目錄是否存在
- 確認是否有寫入權限
- 使用 `--backup` 參數查看當前資料庫位置

### 2. 端口被占用
- 使用 `--port` 參數指定其他端口
- 檢查是否有其他服務使用該端口

### 3. 資料庫損壞
1. 停止應用程序
2. 從備份目錄恢復最近的備份
3. 重新啟動應用程序
