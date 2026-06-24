FROM python:3.13-alpine

# 安裝資料庫編譯必要的基礎系統套件
RUN apk add --no-cache mariadb-connector-c-dev build-base gcc musl-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 🌟 這裡改成 8001
EXPOSE 8001

# 🌟 啟動命令的 Port 也要改成 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
