# 🔐 FastAPI OTP Verification Boilerplate

A ready-to-use backend for email-based OTP login/verification using FastAPI, Celery, Redis, and Gmail SMTP.

---

## ✅ Features

- 🔄 Asynchronous OTP sending using **Celery**
- 📩 Email delivery via **SMTP (Gmail)**
- 🧠 Stateless OTP storage using **Redis**
- 🚦 Real-time **task status tracking** via `/otp-status/{task_id}`
- 📦 Easy to plug into any project

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/otp-service.git
cd otp-service
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Add .env
```bash
GMAIL_ACCOUNT=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
```

### 3. Run services
```bash
# Terminal 1
redis-server

# Terminal 2
celery -A background.celery_app worker --loglevel=info

# Terminal 3
uv run main.py
```

## 💬 API Endpoints
