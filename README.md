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
