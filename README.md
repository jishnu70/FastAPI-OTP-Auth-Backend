# FastAPI OTP Auth Backend 🚀

A backend project for OTP-based authentication using FastAPI, Redis, Celery, and JWT. Built with scalability, modularity, and real-world patterns in mind.

---

### ✨ Features
- Register users with email OTP verification
- Login flow secured via access & refresh tokens
- Password hashing with bcrypt
- OTP sending using Celery + Redis in background
- Async SQLAlchemy + SQLite (swap with PostgreSQL easily)
- Clean folder structure and reusable components

---

### 📦 Stack
- **FastAPI** (async web framework)
- **Redis** (task queue backend)
- **Celery** (background OTP sender)
- **SQLite** + **SQLAlchemy (async)**
- **JWT** for secure token handling
- **Uvicorn** as the ASGI server
- **Passlib** for password hashing
- **Pydantic v2**

---

### 🚀 Getting Started

1. **Clone the repository:**
  ```bash
  git clone https://github.com/jishnu70/FastAPI-OTP-Auth.git
  ```

2. **Install dependencies**
   ```bash
   uv pip install
   ```

3. **Set environment variables**
   Create a `.env` file at root:
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./data.db
   SECRET_KEY=your-secret-key
   JWT_ALGORITHM=HS256
   MAIL_ACCOUNT=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

4. **Run Redis**
   ```bash
   redis-server
   ```

5. **Run Celery**
   ```bash
   celery -A app.background.celery_app worker --loglevel=info
   ```

6. **Start the API**
   ```bash
   uv run app/main.py
   ```

---

### 📁 Folder Structure

```
app/
├── authentication/      # Services & token logic
├── background/          # Celery tasks & OTP logic
├── dependencies/        # DI utils (e.g., current user)
├── infrastructure/      # Redis client setup
├── models/              # SQLAlchemy models
├── routes/              # API routes
├── schemas/             # Pydantic schemas
├── config.py            # App settings
├── database.py          # DB engine/session
└── main.py              # App entry point
```

---

### 🧪 Notes
- You can test this with Postman, Thunder Client, etc.
- Uses [`uv`](https://github.com/astral-sh/uv) instead of `requirements.txt` for dependency management
- OTPs expire in 5 minutes (set in Redis)
- Designed for learning, but with production-aligned structure

---

### 📌 Next Steps
- [ ] Add rate limiting
- [ ] Add resend OTP flow
- [ ] Add password reset via OTP
- [ ] Add logging in JSON format

---

**Built with learning, intention, and a focus on writing clean backend code.**
Think of it as your backend backpack — light, useful, and ready for the road ahead.
