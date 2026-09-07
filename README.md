# Messaging Gateway

FastAPI service that receives WhatsApp (Meta Cloud API) webhook events, persists them, and runs a LangGraph agent (intent detection → FAQ / answer / feedback / greeting / other) to generate and send replies. Two processes share the same codebase: the HTTP API and a Redis-stream worker that dispatches domain events to subscribers.

## Tech stack

| Layer | Technology |
|---|---|
| Language / runtime | Python **3.13.0** (matches `compose/app/Dockerfile` and `compose/worker/Dockerfile`) |
| Web framework | FastAPI 0.136 + Uvicorn |
| Database | PostgreSQL 16 with `pgvector` (`pgvector/pgvector:pg16`) |
| ORM / migrations | SQLAlchemy 2.0 (async, imperative mapping) + Alembic |
| Queue / event bus | Redis 7 Streams (consumer groups) |
| Agent / LLM | LangGraph + LangChain + OpenAI (`langchain-openai`) |
| Auth | JWT (PyJWT) + Argon2 password hashing |
| Messaging channel | WhatsApp Cloud API (Meta) |
| Reverse proxy (prod) | Caddy |
| Testing | pytest + pytest-asyncio |

## Prerequisites

- **Python 3.13** — this repo has no `.python-version`, so activate the interpreter explicitly. [pyenv](https://github.com/pyenv/pyenv) + [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is the workflow this project is built around:
  ```bash
  pyenv install 3.13.0
  pyenv virtualenv 3.13.0 messaging-gateway
  pyenv shell messaging-gateway
  ```
- **Docker + Docker Compose** — for Postgres/Redis (dev) or the full stack (prod-like).
- An **OpenAI API key** if you want the agent (FAQ answering, intent detection) to actually respond.
- A **Meta WhatsApp Cloud API** app (phone number ID + access token) if you want to send/receive real WhatsApp messages. Everything else (auth, conversations, messages, FAQs, business prompts) works without it.

## Quickstart (local dev)

This is the fastest path: infra in Docker, app/worker run locally so `--reload` and breakpoints work.

```bash
# 1. Environment
cp .env.example .env
# edit .env — at minimum set SECRET_KEY, WA_VERIFY_TOKEN, and OPENAI_API_KEY if you'll exercise the agent

# 2. Install dependencies into the pyenv virtualenv
pyenv shell messaging-gateway
pip install -r requirements.txt

# 3. Start Postgres (pgvector) + Redis + RedisInsight
docker-compose -f docker-compose-dev.yml up -d

# 4. Apply migrations (creates tables + the pgvector extension) and seed roles/permissions/channels
alembic upgrade head
python scripts/seed.py

# 5. Create the Redis consumer group used by the worker (one-time, per stream)
PYTHONPATH=. python scripts/create_redis_group.py

# 6. Run the API
uvicorn fast_app.main:app --reload

# 7. In a second terminal, run the event worker
PYTHONPATH=. python workers/redis_worker.py
```

The API is now at `http://localhost:8000` — interactive docs at `/docs` (Swagger UI) and `/redoc`.

## Environment variables

Copy `.env.example` to `.env` and fill in real values — see that file for the full list with inline comments. Groups:

- **App** — `LOG_LEVEL`, `LOG_FORMAT`, `SQL_ECHO`
- **PostgreSQL** — `POSTGRES_DIALECT`, `POSTGRES_DRIVER`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- **Redis** — `REDIS_HOST`, `REDIS_PORT`, `MESSAGE_QUEUE_NAME` (stream name), `MESSAGE_GROUP_NAME` (consumer group)
- **Auth** — `SECRET_KEY` (JWT signing), `AUTH_MAX_ATTEMPTS` / `AUTH_ATTEMPT_WINDOW_SECONDS` / `AUTH_BLOCK_TIME_SECONDS` (login throttling), `PASSWORD_RECOVERY_TIME_SECONDS`
- **Password recovery email** — `FRONTEND_URL`, `EMAIL_USER`, `EMAIL_PASS`
- **Meta / WhatsApp** — `WA_VERIFY_TOKEN` (webhook handshake), `WA_API_URL`, `WA_API_TOKEN`, `WA_PHONE_NUMBER_ID`
- **OpenAI** — `OPENAI_API_KEY`, `OPENAI_CHAT_MODEL`
- **Docker volumes** — `POSTGRES_DATA`, `REDIS_DATA`, `REDISINSIGHT_DATA`, `CADDY_DATA`, `CADDY_CONFIG` (only used by the `docker-compose*.yml` files, not by the app itself)

## Database

Migrations live in `alembic/versions/`. The first migration creates the `vector` extension, so a plain `alembic upgrade head` against a fresh database is enough — no manual `CREATE EXTENSION` step needed.

```bash
alembic revision --autogenerate -m "description"   # generate a new migration
alembic upgrade head                                # apply
alembic downgrade -1                                # roll back one
```

`scripts/seed.py` loads `fixtures/*.json` (roles, permissions, role↔permission mappings, channels) with `ON CONFLICT DO NOTHING`, so it's safe to re-run.

## Running tests

```bash
pyenv shell messaging-gateway
pytest                              # full suite
pytest tests/unit/...               # a single file/dir
pytest path/to/test.py::test_name   # a single test
```

- `tests/unit/**` mocks every collaborator — no DB or network involved.
- `tests/integration/**` runs against an in-memory SQLite engine (not Postgres) via the `db_session` fixture.
- `tests/modules/**` covers the LangGraph agent graph.

Known issue: `modules/app/agent/infrastructure/nodes/*.py` have a broken import (`from app.agent.application import ...`) that breaks collection of two test files — deselect them with `--ignore` if you hit it, or fix the import while you're in that area.

## Running with Docker (full stack)

`docker-compose.yml` runs the API, the worker, Postgres, Redis, and Caddy as a reverse proxy — closer to production:

```bash
docker-compose up --build
```

`docker-compose-dev.yml` only runs Postgres, Redis, and RedisInsight (`http://localhost:5540`) — use it when you want to run the API/worker locally instead (see Quickstart above).

## API

Once running, explore the full contract interactively:

- Swagger UI — `http://localhost:8000/docs`
- ReDoc — `http://localhost:8000/redoc`

All business endpoints are namespaced under `/api/v1`, JSON responses follow the envelope `{"success": bool, "message": str, "data": ...}`, and most reads are permission-gated (JWT bearer token from `/api/v1/login`).

| Method | Path | Notes |
|---|---|---|
| GET | `/api/v1/health` | liveness check |
| GET / POST | `/api/v1/meta/webhook` | WhatsApp Cloud API webhook (verification + inbound events) |
| POST | `/api/v1/login` | email/password → access + refresh token |
| POST | `/api/v1/logout` | revokes a refresh token |
| POST | `/api/v1/refresh-token` | exchanges a refresh token for a new access token |
| POST | `/api/v1/forgot-password` / `/api/v1/reset-password` | password recovery flow |
| GET | `/api/v1/conversation`, `/api/v1/conversation/{id}` | list/detail, paginated |
| GET | `/api/v1/conversation/{id}/message` | messages in a conversation + its detail |
| GET | `/api/v1/channel-account` | paginated |
| GET | `/api/v1/contact` | paginated |
| GET | `/api/v1/faq` | paginated, filterable by `question`/`service` |
| GET | `/api/v1/business-prompt` | prompts for the authenticated user's business (unpaginated) |

## Project structure

Business logic lives under `modules/`, split into `modules/app/*` (bounded contexts: `agent`, `business_prompt`, `channel_account`, `contact`, `conversation`, `faq`, `llm`, `message`, `message_channel`, `webhook_event`) and `modules/shared/*` (cross-cutting concerns: `auth`, `bus`, `persistence`, `http`, `logger`, `environ`, `password_hasher`). Each bounded context follows the same `domain/` → `application/` → `infrastructure/` layering. The FastAPI app (`fast_app/`) and the worker (`workers/redis_worker.py`) are thin entry points on top of that.

## Author

Pedro González

## License

MIT
