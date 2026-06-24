# 快速開始指南

## 📝 項目概述

這是一個 Django 個人網站，具有實時 MQTT 感測器數據監測、數據庫存儲和圖表可視化功能。

**開發者**: 廖烽均 (B11213032)

## ✨ 主要功能

✅ Django 動態網站服務
✅ MQTT 感測器數據實時讀取（支持 3+ 主題）
✅ 數據持久化到 SQLite 數據庫
✅ 歷史數據折線圖表展示
✅ 原始數據瀏覽和篩選
✅ 組專題連結管理
✅ 響應式網頁設計

## 🚀 快速開始

### 第一步：安裝依賴

```bash
pip install -r requirements.txt
```

### 第二步：數據庫遷移

```bash
python manage.py migrate
```

### 第三步：創建管理員帳戶

```bash
python manage.py createsuperuser
```

按照提示輸入：
- 用戶名: admin
- 電子郵件: admin@example.com
- 密碼: （輸入安全密碼）

### 第四步：啟動開發服務器

```bash
python manage.py runserver 0.0.0.0:8000
```

訪問：
- 網站: http://localhost:8000
- 管理後台: http://localhost:8000/admin

### 第五步：配置感測器（在管理後台）

1. 登入管理後台 (http://localhost:8000/admin)
2. 點擊「感測器類型」
3. 添加新感測器（至少 3 個）

示例感測器配置：

| 名稱 | MQTT 主題 | 單位 | 描述 |
|------|----------|------|------|
| 溫度感測器 | sensor/temperature | °C | 室內溫度 |
| 濕度感測器 | sensor/humidity | % | 室內濕度 |
| CO2 感測器 | sensor/co2 | ppm | 二氧化碳濃度 |

或使用快速初始化：

```bash
python utils.py sample-data
```

### 第六步：配置組專題（可選）

1. 在管理後台點擊「項目連結」
2. 添加新連結，例如：
   - 標題: 我的組專題
   - URL: https://example.com/project
   - 描述: 組專題說明

或使用命令：

```bash
python utils.py add-project "我的組專題" "https://example.com/project"
```

### 第七步：啟動 MQTT 監聽器

在新的終端窗口運行：

```bash
python manage.py mqtt_listener --broker localhost --port 1883
```

## 📊 測試 MQTT 連接

### 使用 mosquitto 工具

確保已安裝 mosquitto：

```bash
# Windows (使用 Chocolatey)
choco install mosquitto

# 或下載: https://mosquitto.org/download/
```

發送測試數據：

```bash
# 溫度數據
mosquitto_pub -h localhost -p 1883 -t sensor/temperature -m "25.5"

# 濕度數據
mosquitto_pub -h localhost -p 1883 -t sensor/humidity -m "65.2"

# CO2 數據
mosquitto_pub -h localhost -p 1883 -t sensor/co2 -m "420"
```

### 使用 Python 測試客戶端

```bash
# 發送單個值
python mqtt_test_client.py --broker localhost --topic sensor/temperature --value 25.5

# 發送隨機值（每秒一次，共 10 次）
python mqtt_test_client.py --broker localhost --topic sensor/temperature \
    --random --random-range 20 30 --repeat 10 --interval 1

# 發送 JSON 格式數據
python mqtt_test_client.py --broker localhost --topic sensor/humidity --value '{"value": 65.2}'
```

## 🛠️ 常用命令

```bash
# 查看所有感測器
python utils.py list-sensors

# 查看項目連結
python utils.py list-projects

# 查看統計信息
python utils.py stats

# 清空所有感測器數據
python utils.py clear-data

# 添加新感測器
python utils.py add-sensor "温度" "sensor/temp" "°C" "温度監測"

# 添加新項目
python utils.py add-project "項目名稱" "https://url" "描述"
```

## 🌐 網站導航

| 頁面 | URL | 功能 |
|------|-----|------|
| 首頁 | / | 顯示最新感測器數據 |
| 儀表板 | /dashboard/ | 所有感測器列表 |
| 感測器詳情 | /sensor/\<id\>/ | 單個感測器圖表 |
| 原始數據 | /raw-data/ | 瀏覽所有原始數據 |
| 組專題 | /projects/ | 專題連結 |
| 關於 | /about/ | 網站說明 |
| 管理後台 | /admin/ | 管理感測器和數據 |

## 📈 數據 API

### 獲取感測器數據（JSON格式）

```
GET /api/sensor/<sensor_id>/data/?days=<days>
```

示例：
```bash
curl http://localhost:8000/api/sensor/1/data/?days=1
```

返回：
```json
{
    "sensor": {
        "id": 1,
        "name": "溫度感測器",
        "unit": "°C",
        "mqtt_topic": "sensor/temperature"
    },
    "timestamps": ["2024-01-01T12:00:00Z", ...],
    "values": [25.5, 26.2, ...],
    "min": 20.5,
    "max": 30.2,
    "avg": 25.8,
    "count": 24
}
```

## 🐛 故障排除

### 1. 連接到 MQTT broker 失敗

**問題**: mqtt_listener 無法連接到 broker

**解決方案**:
- 檢查 broker 是否正在運行
- 確認 IP 地址和端口正確
- 檢查防火牆設置
- 如果使用遠程 broker，確保網絡連接

### 2. 沒有看到感測器數據

**問題**: 網站上沒有顯示感測器數據

**解決方案**:
1. 確認已在管理後台添加感測器
2. 確認 mqtt_listener 正在運行
3. 嘗試發送測試數據（見上方 MQTT 測試部分）
4. 檢查感測器的 MQTT 主題名是否正確
5. 查看 mqtt_listener 的控制台輸出以查看錯誤

### 3. 圖表不顯示

**問題**: Chart.js 圖表未加載

**解決方案**:
- 確認有網絡連接（CDN 加載 Chart.js）
- 檢查瀏覽器開發者工具（F12）的控制台是否有錯誤
- 確認感測器有足夠的數據

### 4. 數據庫錯誤

**問題**: 數據庫遷移或查詢出現錯誤

**解決方案**:
```bash
# 重置數據庫
rm db.sqlite3
python manage.py migrate

# 重新創建管理員帳戶
python manage.py createsuperuser
```

## 🔐 安全建議

在生產環境中：

1. 更改 Django SECRET_KEY
2. 設置 DEBUG = False
3. 配置適當的 ALLOWED_HOSTS
4. 使用 HTTPS
5. 設置 MQTT 身份驗證
6. 定期備份數據庫

## 📚 項目結構

```
web/
├── manage.py              # Django 管理腳本
├── requirements.txt       # Python 依賴
├── utils.py              # 工具指令碼
├── mqtt_test_client.py   # MQTT 測試客戶端
├── SETUP_GUIDE.md        # 完整設置指南
├── db.sqlite3            # 數據庫文件
│
├── mysite/               # Django 項目設置
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── mainapp/              # 主應用
    ├── models.py         # 數據模型
    ├── views.py          # 視圖函數
    ├── urls.py           # URL 路由
    ├── admin.py          # 管理後台配置
    │
    ├── management/
    │   └── commands/
    │       └── mqtt_listener.py  # MQTT 監聽服務
    │
    ├── migrations/       # 數據庫遷移
    │
    └── templates/mainapp/
        ├── index.html         # 首頁
        ├── dashboard.html     # 儀表板
        ├── sensor_detail.html # 感測器詳情
        ├── raw_data.html      # 原始數據
        ├── projects.html      # 組專題
        ├── about.html         # 關於頁面
        └── error.html         # 錯誤頁面
```

## 🎯 下一步

1. ✅ 安裝依賴
2. ✅ 運行遷移
3. ✅ 創建管理員帳戶
4. ✅ 添加感測器配置
5. ✅ 啟動 mqtt_listener
6. ✅ 發送 MQTT 測試數據
7. ✅ 訪問網站查看數據

## 📞 需要幫助？

查閱 [SETUP_GUIDE.md](SETUP_GUIDE.md) 獲取更詳細的說明。

---

**最後更新**: 2024年
**開發者**: 廖烽均 (B11213032)
