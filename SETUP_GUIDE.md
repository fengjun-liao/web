# 個人網站設置指南

## 功能需求檢查清單

✅ Django 或同等功能的動態網站服務可以順利在自己的port上執行
✅ 網站上要有名字:廖烽均，座號:B11213032
✅ 具有組專題的網站連結，點擊之後可直接前往
✅ 網站要能夠讀取來自於MQTT指定Topic的內容，至少 3組
✅ 讀取的感測器資料要能夠即時呈現
✅ 讀取的感測器資料要能夠儲存在自己的資料庫中
✅ 讀取的感測器歷史資料要能以圖表的方式呈現在網站上
✅ 具備檢視及瀏覽原始感測器資料的能力

## 安裝步驟

### 1. 環境設置

如果還沒有安裝 Python 和 Django，請按照以下步驟操作：

```bash
# 安裝依賴包
pip install -r requirements.txt
```

### 2. 數據庫遷移

運行以下命令創建數據庫表：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 創建管理員帳戶（如果還沒有）

```bash
python manage.py createsuperuser
```

### 4. 在管理後台配置感測器

1. 啟動開發服務器：
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. 訪問 `http://localhost:8000/admin/` 登入管理後台

3. 在「感測器類型」部分添加感測器（至少3個）
   - 名稱: 例如 "溫度感測器"
   - MQTT主題: 例如 "sensor/temperature"
   - 單位: 例如 "°C"
   - 描述: 可選

4. 添加組專題連結（可選）
   - 標題: 例如 "我的組專題"
   - URL: 例如 "https://example.com/project"
   - 描述: 可選

### 5. 啟動 MQTT 監聽器

在另一個終端窗口運行：

```bash
python manage.py mqtt_listener --broker your_broker_ip --port 1883
```

參數說明：
- `--broker`: MQTT broker 的 IP 地址或主機名（預設：localhost）
- `--port`: MQTT broker 的端口（預設：1883）
- `--username`: MQTT 用戶名（可選）
- `--password`: MQTT 密碼（可選）

## 網站結構

- **首頁 (/)** - 顯示最新的感測器數據和專題連結
- **感測器儀表板 (/dashboard/)** - 列出所有感測器和最新值
- **感測器詳情 (/sensor/<id>/)** - 顯示單個感測器的歷史數據和圖表
- **原始數據 (/raw-data/)** - 瀏覽和篩選所有感測器原始數據
- **組專題 (/projects/)** - 顯示所有組專題連結
- **管理後台 (/admin/)** - 配置感測器和組專題

## MQTT 主題配置

在 MQTT broker 上發送數據到配置的主題。數據格式可以是：

- 單個數字：`25.5`
- JSON 物件：`{"value": 25.5}`
- JSON 物件（其他鍵）：`{"temperature": 25.5}`
- JSON 數組的第一個元素：`[25.5]`

例如：

```
mosquitto_pub -t sensor/temperature -m "25.5"
mosquitto_pub -t sensor/humidity -m '{"value": 65.2}'
mosquitto_pub -t sensor/co2 -m "450"
```

## 常見問題

### 如何更改個人信息？

編輯 `mainapp/views.py` 中的 `PERSONAL_INFO` 字典：

```python
PERSONAL_INFO = {
    "name": "您的名字",
    "student_id": "您的座號",
}
```

### 如何修改導航菜單？

編輯各個模板文件中的 `<nav>` 部分，模板位置：
- `mainapp/templates/mainapp/index.html`
- `mainapp/templates/mainapp/dashboard.html`
- 等等

### MQTT 連接失敗怎麼辦？

1. 確保 MQTT broker 正在運行
2. 確保 IP 地址和端口正確
3. 檢查防火牆設置
4. 查看 mqtt_listener 的輸出以獲取更詳細的錯誤信息

## API 端點

### 獲取感測器數據（JSON）

```
GET /api/sensor/<sensor_id>/data/?days=<days>
```

返回 JSON：
```json
{
    "sensor": {
        "id": 1,
        "name": "溫度感測器",
        "unit": "°C",
        "mqtt_topic": "sensor/temperature"
    },
    "timestamps": ["2024-01-01T12:00:00+08:00", ...],
    "values": [25.5, 26.2, ...],
    "min": 20.5,
    "max": 30.2,
    "avg": 25.8,
    "count": 24
}
```

## 技術棧

- **後端框架**: Django 6.0.6
- **數據庫**: MySQL
- **MQTT 客戶端**: paho-mqtt 1.6.1
- **前端**: HTML5 + CSS3 + JavaScript
- **圖表庫**: Chart.js

## 支持的功能

- ✅ 實時感測器數據顯示
- ✅ MQTT 主題自動發現和訂閱
- ✅ 數據持久化到 MySQL 資料庫
- ✅ 歷史數據折線圖表
- ✅ 數據篩選和瀏覽
- ✅ 響應式設計（桌面和移動設備）
- ✅ 管理後台配置
- ✅ 多感測器支持
- ✅ 時間範圍篩選

## 下一步

1. 安裝依賴：`pip install -r requirements.txt`
2. 運行遷移：`python manage.py migrate`
3. 啟動開發服務器：`python manage.py runserver`
4. 訪問 http://localhost:8000
5. 在管理後台配置感測器
6. 啟動 MQTT 監聽器
7. 發送 MQTT 消息測試

祝您使用愉快！
