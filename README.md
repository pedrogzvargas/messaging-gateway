# 🚀 FastAPI Backend – Docker + Alembic

Backend API built with **FastAPI**, using **SQLAlchemy** as the ORM and **Alembic** for database migrations.  
The project is fully containerized with **Docker** and orchestrated using **Docker Compose** for a consistent and reproducible development environment.

---

## 🧰 Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker
- Docker Compose

---

## 📁 Project Structure

```text
.
├── app/
│   ├── api/              # API routers
│   ├── models/           # SQLAlchemy models
│   ├── db/
│   │   ├── base.py       # Declarative Base
│   │   └── session.py   # Engine and session
│   ├── core/             # App configuration
│   └── main.py           # FastAPI entry point
├── alembic/
│   ├── versions/         # Migration files
│   └── env.py
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file at the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/app_db
```

---

## 🐳 Run the Project (Docker Compose)

```bash
docker-compose up --build
```

API available at:

```text
http://localhost:8000
```

---

## 📘 API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🔄 Database Migrations

Ensure vector type exist

```bash
CREATE EXTENSION IF NOT EXISTS vector;
```

```bash
docker-compose exec api alembic revision --autogenerate -m "migration description"
docker-compose exec api alembic upgrade head
docker-compose exec api alembic downgrade -1
```

---

## 🔐 Root Access

```bash
docker-compose exec --user 0 api /bin/bash
```

---

## 🧪 Local Development

```bash
uvicorn app.main:app --reload
```

---

## 📌 Author

Pedro González

---

## 📄 License

MIT
