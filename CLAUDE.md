# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Avangard — система управления строительством (construction management system). Full-stack web app with Russian-language UI. Three user roles: **admin** (full access), **master** (site manager, scoped to their address), **common** (employee, basic access).

## Commands

### Backend (from `backend/`)

```bash
# Run dev server
source venv/bin/activate && uvicorn src.main:app --reload

# Database migrations
alembic upgrade head

# Reset DB (drops and recreates all tables)
# POST http://localhost:8000/v1/health/setup_db
```

No tests or linter configured for the backend.

### Frontend (from `frontend/Avangard/`)

```bash
npm install          # Install dependencies
npm run dev          # Vite dev server
npm run build        # Type-check + build
npm run test:unit    # Vitest
npm run test:e2e     # Playwright
npm run lint         # oxlint + eslint (--fix --cache)
npm run format       # Prettier
npm run type-check   # vue-tsc
```

Node: `^20.19.0 || >=22.12.0`

## Architecture

### Backend — `backend/src/`

Layered FastAPI app with async SQLAlchemy 2.0:

- **`api/v1/`** — REST endpoints under `/v1/`. FastAPI dependency injection for auth and services.
- **`services/`** — Business logic. Each service receives an `AsyncSession`. Services log actions via `EventJournalService`.
- **`models/`** — SQLAlchemy ORM models with `Mapped` annotations. 5 tables: `users`, `addresses`, `tasks`, `storage`, `event_journal`.
- **`schemas/`** — Pydantic v2 request/response models.
- **`dependencies/`** — Auth deps (`CurrentUser`, `AdminUser`, `ManagerOrAdminUser`) and service injection.
- **`core/`** — Config, Redis caching with `@cached(ttl=...)` decorator.

**Auth**: JWT (HS256, 30-min expiry) via `python-jose`. Passwords: argon2 via `passlib`. Token blacklist is in-memory dict (resets on server restart).

**Caching**: Redis with graceful degradation if unavailable. Pattern-based cache invalidation.

**Background task**: `asyncio` loop every 24h marks overdue tasks as "Просрочено".

### Frontend — `frontend/Avangard/src/`

Vue 3 SPA with Composition API:

- **`stores/`** — Pinia stores (`auth`, `tasks`, `storage`). API calls use raw `fetch()` to `http://0.0.0.0:8000/v1/...`.
- **`views/`** — `Login.vue`, `Dashboard.vue`.
- **`layouts/`** — `DashboardLayout.vue` wraps dashboard with sidebar + topbar.
- **`components/`** — StatCard, WarehouseCard, TasksBoard, StaffCard, EventJournal, OverdueTasksModal, LowMaterialsModal, Sidebar, Topbar.
- **`router/`** — Two routes: `/login` and `/dashboard` (auth guard).

**Styling**: Tailwind CSS. Brand color: `#1F5D3A`.

## Key Conventions

- Backend API base: `http://0.0.0.0:8000` (hardcoded in frontend stores/components, no env var).
- DB: PostgreSQL with asyncpg. Connection string in `backend/.env`.
- `alembic.ini` uses sync PG URL (`postgresql://`) while the app uses async (`postgresql+asyncpg://`) from `.env`.
- `backend/requirements.txt` is currently empty — dependencies only exist in venv.
- Frontend login currently restricts to `admin` role only, though backend supports `master` and `common`.
