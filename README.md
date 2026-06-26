# 廖烽均個人網站 - IoT 感測器監測系統

## 📋 專案描述

這是一個功能完整的 Django 個人網站，用於實時監測和可視化 IoT 感測器數據。網站通過 MQTT 協議讀取多個感測器的數據，並儲存到 MySQL 資料庫，提供實時顯示、圖表分析和原始數據瀏覽等功能。

**開發者**: 廖烽均  
**座號**: B11213032

## ✅ 功能需求實現檢查表

- ✅ **Django 或同等功能的動態網站服務可以順利在自己的port上執行**
  - 使用 Django 6.0.6 框架
  - 支持自定義端口運行（默認 8000）

- ✅ **網站上要有名字和座號**
  - 首頁顯示：廖烽均，座號：B11213032
  - 所有頁面頭部均展示

- ✅ **具有組專題的網站連結，點擊之後可直接前往**
  - `/projects/` 頁面展示所有組專題連結
  - 首頁也有快捷鏈接
  - 管理後台可管理專題連結

- ✅ **網站要能夠讀取來自於MQTT指定Topic的內容，至少 3組**
  - mqtt_listener 管理命令自動訂閱和監聽 MQTT 主題
  - 支持無限個感測器主題
  - 自動發現新主題功能

- ✅ **讀取的感測器資料要能夠即時呈現**
  - `/` 首頁實時顯示所有感測器最新數據
  - `/dashboard/` 儀表板展示所有感測器
  - 實時更新每個感測器的最新值

- ✅ **讀取的感測器資料要能夠儲存在自己的資料庫中**
  - SensorData 模型存儲每個讀數
  - 自動時間戳和感測器關聯
  - MySQL 資料庫持久化存儲

- ✅ **讀取的感測器歷史資料要能以圖表的方式呈現在網站上**
  - Chart.js 折線圖表顯示歷史數據
  - `/sensor/<id>/` 頁面顯示單個感測器圖表
  - 支持按時間範圍篩選（1天、7天、30天）

- ✅ **具備檢視及瀏覽原始感測器資料的能力**
  - `/raw-data/` 頁面提供完整的原始數據瀏覽
  - 支持按感測器和時間範圍篩選
  - 顯示前 1000 筆記錄

## 🎯 核心功能

### 1. 實時感測器數據監測
- 通過 MQTT 協議實時讀取感測器數據
- 支持多種數據格式：純數字、JSON、數組
- 自動保存到數據庫

### 2. 數據可視化
- 折線圖表展示歷史數據趨勢
- 統計信息：最小值、最大值、平均值
- 多時間範圍篩選

### 3. 數據管理
- 完整的 Django 管理後台
- 感測器類型管理
- 組專題連結管理
- 原始數據瀏覽和統計

### 4. 響應式設計
- 適配桌面、平板、手機設備
- 現代化 UI 設計
- 快速加載性能

## 🚀 快速開始

### 最小化安裝（3 步）

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 數據庫遷移
python manage.py migrate

# 3. 啟動服務器
python manage.py runserver 0.0.0.0:8000
```

訪問 http://localhost:8000

### 完整設置（7 步）

詳見 [QUICKSTART.md](QUICKSTART.md) 或 [SETUP_GUIDE.md](SETUP_GUIDE.md)

### 示例配置

```bash
# 創建管理員帳戶
python manage.py createsuperuser

# 創建示例感測器和項目
python utils.py sample-data

# 啟動 MQTT 監聽器
python manage.py mqtt_listener --broker localhost --port 1883

# 發送測試數據
python mqtt_test_client.py --broker localhost --topic sensor/temperature --value 25.5
```

## 📁 項目結構

```
web/
├── README.md              # 本文件
├── QUICKSTART.md          # 快速開始指南
├── SETUP_GUIDE.md         # 完整設置指南
├── requirements.txt       # Python 依賴
├── utils.py               # 工具腳本
├── mqtt_test_client.py    # MQTT 測試客戶端
├── manage.py              # Django 管理
├── （使用 MySQL，資料庫設定在 mysite/settings.py）
│
├── mysite/                # Django 項目配置
│   ├── settings.py        # 設置
│   ├── urls.py            # URL 路由
│   ├── asgi.py            # ASGI 配置
│   └── wsgi.py            # WSGI 配置
│
└── mainapp/               # 主應用
    ├── models.py          # 數據模型 (SensorType, SensorData, ProjectLink)
    ├── views.py           # 視圖函數
    ├── urls.py            # URL 路由
    ├── admin.py           # 管理後台配置
    ├── apps.py            # 應用配置
    ├── tests.py           # 單元測試
    │
    ├── management/commands/
    │   └── mqtt_listener.py        # MQTT 監聽服務
    │
    ├── migrations/
    │   ├── 0001_initial.py         # 初始遷移
    │   └── __init__.py
    │
    └── templates/mainapp/
        ├── index.html              # 首頁 (/)
        ├── dashboard.html          # 儀表板 (/dashboard/)
        ├── sensor_detail.html      # 感測器詳情 (/sensor/<id>/)
        ├── raw_data.html           # 原始數據 (/raw-data/)
        ├── projects.html           # 組專題 (/projects/)
        ├── about.html              # 關於 (/about/)
        └── error.html              # 錯誤頁面
```

## 🛠️ 技術堆棧

- **框架**: Django 6.0.6
- **數據庫**: MySQL
- **MQTT**: paho-mqtt 1.6.1
- **Python**: 3.8+

### 前端
- **HTML5**: 結構化標記
- **CSS3**: 響應式設計
- **JavaScript**: 交互和數據加載
- **Chart.js**: 數據可視化

## 📊 數據模型

### SensorType（感測器類型）
- `name`: 感測器名稱
- `mqtt_topic`: MQTT 主題
- `unit`: 單位（如 °C、%、ppm）
- `description`: 描述
- `created_at`: 創建時間

### SensorData（感測器數據）
- `sensor`: 外鍵關聯到 SensorType
- `value`: 數值
- `timestamp`: 時間戳

### ProjectLink（項目連結）
- `title`: 項目標題
- `url`: 項目 URL
- `description`: 描述
- `created_at`: 創建時間

## 🔌 MQTT 集成

### 監聽服務

```bash
python manage.py mqtt_listener \
    --broker your_broker_ip \
    --port 1883 \
    --username optional_user \
    --password optional_pass
```

### 支持的數據格式

```
純數字: 25.5
JSON 物件: {"value": 25.5}
JSON 物件: {"temperature": 25.5}
JSON 數組: [25.5, 26.2]
```

### 測試 MQTT

```bash
# 使用 mosquitto
mosquitto_pub -t sensor/temperature -m "25.5"

# 使用 Python 工具
python mqtt_test_client.py --broker localhost --topic sensor/temp --value 25.5
```

## 🌐 API 端點

| 方法 | 端點 | 功能 |
|------|------|------|
| GET | `/` | 首頁 |
| GET | `/dashboard/` | 儀表板 |
| GET | `/sensor/<id>/` | 感測器詳情 |
| GET | `/api/sensor/<id>/data/` | 感測器數據 (JSON) |
| GET | `/raw-data/` | 原始數據瀏覽 |
| GET | `/projects/` | 組專題 |
| GET | `/about/` | 關於頁面 |
| GET | `/admin/` | 管理後台 |

### API 數據格式

```json
GET /api/sensor/1/data/?days=1

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

## 🛠️ 管理工具

### utils.py - 工具腳本

```bash
# 查看所有感測器
python utils.py list-sensors

# 查看項目連結
python utils.py list-projects

# 查看統計信息
python utils.py stats

# 添加感測器
python utils.py add-sensor "溫度" "sensor/temp" "°C"

# 添加項目
python utils.py add-project "項目名" "https://url"

# 創建示例數據
python utils.py sample-data

# 清空所有數據
python utils.py clear-data
```

## 📱 頁面說明

### 首頁 (/)
- 顯示個人信息（名字、座號）
- 實時顯示所有感測器最新數據
- 快速訪問所有功能的導航

### 儀表板 (/dashboard/)
- 表格形式列出所有感測器
- 顯示最新值和記錄總數
- 快速訪問感測器詳情

### 感測器詳情 (/sensor/<id>/)
- 顯示單個感測器的詳細信息
- 折線圖表展示歷史數據
- 時間範圍篩選（1天、7天、30天）
- 統計信息（最小值、最大值、平均值）

### 原始數據 (/raw-data/)
- 瀏覽所有感測器的原始數據
- 按感測器篩選
- 按時間範圍篩選
- 支持查看前 1000 筆記錄

### 組專題 (/projects/)
- 顯示所有配置的組專題連結
- 卡片式設計，點擊可直接前往

### 關於 (/about/)
- 網站功能介紹
- 技術棧說明
- 使用指南
- 故障排除

## 🔐 安全性

### 開發環境
- DEBUG = True（開發中使用）
- 簡單的 SECRET_KEY

### 生產環境建議
1. 更改 SECRET_KEY
2. 設置 DEBUG = False
3. 配置 ALLOWED_HOSTS
4. 使用 HTTPS
5. 設置 MQTT 身份驗證
6. 定期備份數據庫
7. 使用環境變量存儲敏感信息

## 🐛 常見問題

**Q: MQTT 連接失敗**
A: 檢查 broker IP、端口、防火牆設置

**Q: 看不到感測器數據**
A: 確認已添加感測器、mqtt_listener 正在運行、發送了 MQTT 消息

**Q: 圖表不顯示**
A: 檢查網絡連接、確認有足夠的數據、查看瀏覽器控制台錯誤

**Q: 數據庫錯誤**
A: 運行 `python manage.py migrate`。如需重置資料庫，請在 MySQL 中刪除並重建專案對應的資料庫，或清空表後重新執行遷移。

詳見 [SETUP_GUIDE.md](SETUP_GUIDE.md#🐛-故障排除) 中的完整故障排除指南

## 📈 性能優化

- 數據庫索引：timestamp 和 sensor 字段
- 分頁：原始數據限制為 1000 筆
- 緩存就緒（可配置 Django 緩存）
- CDN 加載 Chart.js

## 🚢 部署建議

### 在 Linux 服務器上部署

```bash
# 使用 Gunicorn 和 Nginx
pip install gunicorn
gunicorn mysite.wsgi --bind 0.0.0.0:8000

# 後台運行 MQTT 監聽器
nohup python manage.py mqtt_listener &
```

### Docker 容器化

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:8000
```

## 📚 文檔

- [QUICKSTART.md](QUICKSTART.md) - 快速開始指南
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 完整設置指南
- [此 README](#) - 項目概述

## 📞 聯絡信息

**開發者**: 廖烽均  
**座號**: B11213032

## 📄 許可證

MIT License

## 🙏 致謝

感謝 Django、MQTT、Chart.js 等開源項目的支持。

---

**最後更新**: 2024年  
**版本**: 1.0.0
