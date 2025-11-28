# 📊 Diabetes Data Pipeline (Docker + PostgreSQL + ETL + pgAdmin)

โปรเจกต์นี้เป็นระบบประมวลผลข้อมูลผู้ป่วยโรคเบาหวาน  
ตั้งแต่ขั้นตอน **Ingest → Transform → Load → Explore** โดยใช้ Docker Compose เพื่อรันทุก service แบบครั้งเดียว

---
## 🚀 Features
- PostgreSQL Database
- pgAdmin สำหรับดูตารางและ Query ข้อมูล
- Python
- ใช้ pgAdmin เชื่อมต่อ Database

---
## ⚙️ Requirements
จำเป็นต้องติดตั้ง:
- Docker
- Docker Compose
- pgAdmin (optional)
- DBeaver (optional)

---
# ▶️ How to Run

## 1️⃣ Clone Repository
```bash
git clone https://github.com/bumkin01/diabetes-pipeline.git
cd diabetes-pipeline
```

## 2️⃣ Start All Services
```bash
docker compose up --build
```

## 3️⃣ PostgreSQL Info
| Item     | Value         |
| -------- | ------------- |
| Host     | `localhost`   |
| Port     | `5432`        |
| Username | `postgres`    |
| Password | `postgres`    |
| Database | `diabetes_db` |

## 4️⃣ Connect Database
1. pgAdmin

เปิดเว็บไซต์ pgAdmin
👉 http://localhost:8080

| Email                                     | Password |
| ----------------------------------------- | -------- |
| [admin@admin.com](mailto:admin@admin.com) | admin    |

Add New Server
- Host: db
- Port: 5432
- User: postgres
- Password: postgres

หลังจากเชื่อมจะเห็นตาราง:
```bash
raw_data_diabetes
clean_data_diabetes
```

2. DBeaver
ตั้งค่าการเชื่อมต่อ:

- Host: db
- Port: 5432
- Database: diabetes_db
- User: postgres
- Password: postgres

## 5️⃣ Disconnect 
```bash
docker compose down
```