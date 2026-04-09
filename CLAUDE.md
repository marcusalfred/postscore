# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

**With Docker (recommended):**
```bash
docker compose up --build -d
```
- API: `http://localhost:8000` — Docs at `http://localhost:8000/docs`
- Web UI: `http://localhost:3000`

**Web UI locally (without Docker):**
```bash
cd web
npm install
npm run dev   # http://localhost:3000
```
Requires `web/.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`.

**Locally with uvicorn:**
```bash
cd app
pip install -r requirements.txt
cp ../example.env .env  # then fill in DB credentials
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Environment variables** (see `example.env`): `DB_NAME`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`. Note: `db/database.py` reads `DB_*` vars; `core/config.py` reads `POSTGRES_*` vars — both sets may be needed depending on which module is reached.

## Database

PostgreSQL is required. Alembic is the single source of truth for the schema — `init_schema.sql` is kept only for reference and is no longer applied automatically.

On first startup (Docker or local), run migrations to create all tables:
```bash
# From repo root
alembic upgrade head
```

Docker handles this automatically — `alembic upgrade head` runs before uvicorn on every container start.

To seed development data after migrations:
```bash
# Against the Docker DB
docker exec -i postscore_db psql -U postgres -d postscore < seed_data.sql

# Against a local DB
psql -U postgres -d postscore -f seed_data.sql
```

To generate a new migration after changing a model:
```bash
alembic revision --autogenerate -m "describe the change"
```

Database backup/restore scripts live in `data_backup/`.

## Architecture

All application code lives under `app/`. The entry point is `app/main.py`, which uses a factory function `create_application()`.

**Layer flow:** Router endpoint → Repository → SQLAlchemy ORM model → PostgreSQL

### Key layers

- **`app/api/v1/endpoints/`** — Route handlers: `auth.py`, `courses.py`, `players.py`, `rounds.py`, `admin.py`. Registered at `/api/v1/` prefix via `app/api/v1/api.py`.
- **`app/repositories/`** — Data access layer. `base.py` provides a generic `BaseRepository[Model, CreateSchema, UpdateSchema]` with `get`, `get_or_404`, `get_multi`, `create`, `update`, `remove`. Domain repos (`course_repository.py`, `player_repository.py`, `round_repository.py`) extend it with custom queries.
- **`app/schemas/pydantic_models.py`** — All Pydantic request/response models in one file.
- **`app/db/models.py`** — SQLAlchemy ORM models (`Player`, `Course`, `TeeBox`, `TeeBoxHole`, `Round`, `RoundHole`). All PKs use ULID (26-char string). `TimestampMixin` adds `created_on`.
- **`app/db/database.py`** — Engine, `SessionLocal`, and `get_db()` FastAPI dependency.
- **`app/core/config.py`** — Pydantic `Settings` class; reads from `.env`.
- **`app/core/security.py`** — JWT (via `python-jose`) + bcrypt password hashing. FastAPI dependencies: `get_current_user`, `get_current_active_user`, `get_current_superuser`.
- **`app/core/errors.py`** — Custom exception hierarchy (`APIException`, `ResourceNotFoundException`, `ValidationException`, `AuthenticationException`, `AuthorizationException`, `DatabaseException`). All are handled globally in `main.py`.

### Auth model

Players authenticate via `POST /api/v1/auth/login` (OAuth2 password flow). JWT token encodes `player.id` as `sub`. `is_super=True` on a `Player` grants superuser access. Admin endpoints are unprotected in development (`ENVIRONMENT != "production"`), protected in production.

## Web UI (`web/`)

Next.js 15 App Router app — a full migration of the Expo UI to web.

- **`web/app/`** — App Router pages. Route groups: `(auth)` for login/signup, `(tabs)` for the main tabbed shell.
- **`web/components/`** — Shared, rounds, and scorecard components (HTML equivalents of the RN originals).
- **`web/lib/`** — API client, auth (localStorage), queries (TanStack Query), storage (localStorage), offline queue.
- **`web/providers/`** — `QueryProvider` and `ThemeProvider` (next-themes) client wrappers.
- Dark mode via `next-themes` with `attribute="class"` — same `dark:` Tailwind classes throughout.
- Offline hole-scoring queue uses `window.addEventListener('online', ...)` to flush on reconnect.

> **Note:** `ui/` (the original Expo app) is kept for reference but is no longer the active frontend. It will be archived once the web app is confirmed solid.

### Data model hierarchy

```
Course → TeeBox (multiple tee colors per course)
       → TeeBoxHole (18 holes per tee box)

Player → Round (references Course + TeeBox)
       → RoundHole (references TeeBoxHole; unique per round+hole)
```
