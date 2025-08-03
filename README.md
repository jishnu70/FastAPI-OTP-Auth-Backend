# 🔐 FastAPI OTP Authentication System

A production-ready email-based authentication system built with **FastAPI**, **Redis**, **Celery**, and **JWT tokens** — designed for modern backend applications with OTP-based email verification.

---

## 🚀 Features

- ✅ Async FastAPI backend using `SQLAlchemy`
- ✅ One-Time Password (OTP) verification via email
- ✅ Redis-backed in-memory OTP storage with expiration
- ✅ Background task processing using Celery + Redis
- ✅ JWT-based access and refresh tokens
- ✅ Modular and extensible folder structure
- ✅ Secure password hashing (`bcrypt`)
- ✅ Clean architecture: models, services, routes, dependencies

---

## 🧰 Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- Celery
- Redis
- smtplib (email sending)
- SQLite (local DB)
- Pydantic v2
- JWT (`pyjwt`)

---

## 📁 Folder Structure

```
project/
├── background/         # Celery app + OTP service
├── routes/             # Auth API routes
├── models/             # SQLAlchemy user model
├── schemas/            # Pydantic request/response models
├── services/           # Business logic
├── utils/              # JWT and security helpers
├── config.py           # Environment config
├── main.py             # Entry point
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo and install dependencies
```bash
git clone https://github.com/yourname/fastapi-otp-auth.git
cd fastapi-otp-auth
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the root:
```
GMAIL_ACCOUNT=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
```

Make sure you [generate an App Password](https://myaccount.google.com/apppasswords) for Gmail.

---

### 3. Start Redis

If Redis isn't running already:

```bash
brew services start redis
```

---

### 4. Run the backend + worker

In **terminal 1**:
```bash
uvicorn main:app --reload
```

In **terminal 2**:
```bash
celery -A background.celery_app worker --loglevel=info
```

---

## 📬 Sample Request Flow

### Register:
```
POST /auth/register
{
  "username": "jishnu",
  "email": "jishnu@example.com",
  "password": "strongpass123",
  "confirm_password": "strongpass123"
}
```

### Verify OTP:
```
POST /auth/verify-otp
{
  "email": "jishnu@example.com",
  "otp": "123456"
}
```

### Login:
```
POST /auth/login
{
  "email": "jishnu@example.com",
  "password": "strongpass123"
}
```

### Refresh Access Token:
```
POST /auth/refresh-token
{
  "refresh_token": "<your_refresh_token>"
}
```

---

## 🛡️ TODO / Future Improvements

- [ ] Rate limiting on OTP send
- [ ] Blacklisting refresh tokens
- [ ] Add user logout endpoint
- [ ] OTP retry limit per IP/email
- [ ] Dockerfile & Redis container
- [ ] Testing with pytest + httpx

---

## 📜 License

This project is licensed under the MIT License.
