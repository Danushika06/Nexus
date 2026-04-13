---
name: fastapi
description: >
  Use this skill whenever building, scaffolding, debugging, or reviewing FastAPI applications
  or Python REST/GraphQL APIs. Triggers include any mention of FastAPI, Uvicorn, Starlette,
  Pydantic models, Python API development, ASGI servers, or async Python web services.
  Also use when the user asks to build a backend API in Python, mentions routers/dependencies/
  middleware in a Python context, references SQLAlchemy with async, Alembic migrations,
  or asks about structuring a Python API project. Covers FastAPI 0.115+, Pydantic v2,
  SQLAlchemy 2.0 async, dependency injection, authentication patterns, background tasks,
  testing, and production deployment with Docker/Uvicorn.
---

# FastAPI Skill — Production Patterns for FastAPI (2025+)

This skill covers building production-grade APIs with FastAPI, leveraging Pydantic v2 for validation, SQLAlchemy 2.0 for async database access, and modern Python (3.11+) features.

---

## 1. Project Structure

For anything beyond a toy project, organize by **domain/module** rather than by file type. This scales from MVP to enterprise.

### Small-to-medium projects (file-type structure)

```
app/
├── main.py              # FastAPI app creation + lifespan
├── config.py            # Settings via pydantic-settings
├── database.py          # Engine, session factory, get_db dependency
├── dependencies.py      # Shared dependencies (auth, pagination, etc.)
├── routers/
│   ├── __init__.py
│   ├── users.py
│   └── items.py
├── schemas/             # Pydantic request/response models
│   ├── user.py
│   └── item.py
├── models/              # SQLAlchemy ORM models
│   ├── user.py
│   └── item.py
├── services/            # Business logic (not in routers)
│   ├── user_service.py
│   └── item_service.py
├── migrations/          # Alembic migrations
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── alembic.ini
├── pyproject.toml
├── Dockerfile
└── .env
```

### Large projects (domain-based structure)

Inspired by Netflix's Dispatch pattern — each domain is self-contained:

```
src/
├── auth/
│   ├── router.py        # Auth endpoints
│   ├── schemas.py       # Pydantic models for auth
│   ├── models.py        # User, Token DB models
│   ├── dependencies.py  # get_current_user, require_admin
│   ├── service.py       # Business logic (hash, verify, JWT)
│   ├── config.py        # Auth-specific settings
│   ├── constants.py     # TOKEN_EXPIRE_MINUTES, etc.
│   ├── exceptions.py    # AuthenticationError, etc.
│   └── utils.py
├── posts/
│   ├── router.py
│   ├── schemas.py
│   ├── models.py
│   ├── dependencies.py
│   ├── service.py
│   └── exceptions.py
├── config.py            # Global settings
├── database.py          # Async engine + session
├── models.py            # Base model, shared mixins
├── exceptions.py        # Global exception handlers
├── middleware.py         # Request logging, CORS, etc.
├── main.py              # App factory + lifespan
└── utils/               # Shared utilities
```

Each domain module owns its own router, schemas, models, and business logic. The global `main.py` imports and mounts routers.

---

## 2. Application Factory Pattern

Use the **application factory** with `lifespan` for clean startup/shutdown:

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import sessionmanager
from app.routers import users, items
from app.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    settings = get_settings()
    await sessionmanager.init(settings.database_url)
    yield
    await sessionmanager.close()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    app.include_router(users.router, prefix="/api/v1")
    app.include_router(items.router, prefix="/api/v1")

    return app


app = create_app()
```

**Why lifespan over `@app.on_event`?** The `on_event` decorators are deprecated. The `lifespan` context manager is the modern approach — it pairs startup with shutdown cleanly and supports dependency injection.

---

## 3. Configuration with Pydantic Settings

```python
# app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "My API"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20

    secret_key: str
    access_token_expire_minutes: int = 30

    allowed_origins: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

- Use `pydantic-settings` (extracted from Pydantic v2) for type-safe env management.
- Cache with `@lru_cache` so settings are loaded once.
- Never hardcode secrets — always read from `.env` or environment.

---

## 4. Async Database Setup (SQLAlchemy 2.0)

```python
# app/database.py
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,       # e.g., "postgresql+asyncpg://..."
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,          # Verify connections before use
    echo=settings.debug,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    """Dependency that yields an async session with auto-commit/rollback."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### ORM model example (SQLAlchemy 2.0 Mapped classes)

```python
# app/models/user.py
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
```

---

## 5. Pydantic v2 Schemas

Pydantic v2 uses a Rust core for up to 50x faster validation. Key changes from v1:

```python
# app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """All fields optional for PATCH updates."""
    email: EmailStr | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Replaces orm_mode=True

    id: int
    email: str
    is_active: bool
    created_at: datetime


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    size: int
```

### Key Pydantic v2 patterns

- `model_config = ConfigDict(from_attributes=True)` — replaces `class Config: orm_mode = True`.
- `model_dump()` replaces `.dict()`.  `model_dump_json()` replaces `.json()`.
- `model_validate()` replaces `.from_orm()`.
- Use `Field()` for constraints: `min_length`, `max_length`, `gt`, `ge`, `pattern`, etc.
- Separate schemas for Create, Update, and Response — don't reuse one model for everything.

---

## 6. Async/Sync Route Rules

This is one of the most common sources of bugs in FastAPI:

```python
# ✅ CORRECT: async route with async I/O
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# ✅ CORRECT: sync route for blocking I/O (FastAPI runs it in a threadpool)
@router.post("/reports/generate")
def generate_report(config: ReportConfig):
    return create_pdf_report(config)  # CPU-bound / blocking library

# ❌ WRONG: blocking call inside an async route — blocks the event loop
@router.post("/process")
async def process_image(file: UploadFile):
    image = cv2.imread(file.file)  # BLOCKS the event loop!
    return heavy_processing(image)

# ✅ FIX: offload CPU-bound work to a thread pool
import asyncio

@router.post("/process")
async def process_image(file: UploadFile):
    data = await file.read()
    result = await asyncio.get_event_loop().run_in_executor(
        None, heavy_processing, data
    )
    return {"result": result}
```

**The rule**: If your route does only async I/O (database, HTTP, file I/O via async libraries), use `async def`. If it calls blocking/sync libraries, use plain `def` (FastAPI auto-runs it in a threadpool). Never mix blocking calls inside `async def` routes.

---

## 7. Dependency Injection

Dependencies are FastAPI's superpower. They are cacheable, composable, and handle cleanup via `yield`.

```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.config import get_settings
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id: int = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


async def require_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
```

### Dependency best practices

- Dependencies with the same parameters are **cached within a single request**. Use this to avoid duplicate DB calls.
- Use `yield` for cleanup (e.g., closing DB sessions).
- Layer dependencies: `get_db` → `get_current_user` → `require_admin`.
- Use dependencies for validation against DB constraints (e.g., "does this entity exist?").

---

## 8. Router Organization

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserListResponse
from app.services.user_service import UserService
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    return await service.list_users(page=page, size=size)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    return await service.create_user(payload)
```

### Router rules

- Keep routes thin — delegate business logic to service classes/functions.
- Always set `response_model` for auto-serialization and OpenAPI docs.
- Use `tags` for logical grouping in Swagger UI.
- Use `status_code` to set non-200 defaults (e.g., `201` for creation).

---

## 9. Service Layer Pattern

Separate business logic from routing:

```python
# app/services/user_service.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, payload: UserCreate) -> User:
        existing = await self.db.execute(
            select(User).where(User.email == payload.email)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def list_users(self, page: int, size: int):
        offset = (page - 1) * size
        total_q = await self.db.execute(select(func.count(User.id)))
        total = total_q.scalar_one()

        result = await self.db.execute(
            select(User).offset(offset).limit(size).order_by(User.created_at.desc())
        )
        items = result.scalars().all()
        return {"items": items, "total": total, "page": page, "size": size}
```

---

## 10. Exception Handling

```python
# app/exceptions.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Log the full traceback here
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
```

Never leak internal error details to clients. Log the full traceback server-side; return a generic message to the client.

---

## 11. Middleware

```python
# app/middleware.py
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        logger.info(
            f"{request.method} {request.url.path} "
            f"status={response.status_code} duration={duration:.3f}s"
        )
        return response
```

Middleware execution order: the **last added** middleware runs **first**. Add CORS middleware after custom middleware if you want CORS headers on error responses.

---

## 12. Background Tasks

For lightweight async work, use FastAPI's built-in `BackgroundTasks`:

```python
from fastapi import BackgroundTasks

@router.post("/users/", status_code=201)
async def create_user(
    payload: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    user = await UserService(db).create_user(payload)
    background_tasks.add_task(send_welcome_email, user.email)
    return user
```

For heavy or long-running jobs (>30s), use **Celery + Redis** or **ARQ** instead.

---

## 13. Testing

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import create_app
from app.database import Base, get_db

TEST_DB_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DB_URL)
TestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    app = create_app()

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


# tests/test_users.py
import pytest

@pytest.mark.anyio
async def test_create_user(client):
    response = await client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "password": "securepassword123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
```

Use `httpx.AsyncClient` with `ASGITransport` — it's the modern replacement for `TestClient` in async contexts. Override dependencies to inject test databases.

---

## 14. Alembic Migrations

```bash
# Initialize Alembic
alembic init migrations

# Generate a migration from model changes
alembic revision --autogenerate -m "add users table"

# Apply migrations
alembic upgrade head
```

Configure `migrations/env.py` to use your async engine and import all models so autogenerate detects them. Always review auto-generated migrations before applying.

---

## 15. Docker & Deployment

```dockerfile
FROM python:3.12-slim AS base

WORKDIR /app

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache -r pyproject.toml

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Production Uvicorn settings

- Use `--workers` (number of CPU cores × 2 + 1 is a common starting point).
- Use `--limit-concurrency` and `--timeout-keep-alive` for stability.
- Put Uvicorn behind a reverse proxy (Nginx, Caddy, or cloud LB) for TLS termination.
- Use `--access-log` for request logging or rely on middleware.

---

## 16. API Versioning

Prefix all routes with `/api/v1/`. When introducing breaking changes, add `/api/v2/` routers alongside v1:

```python
app.include_router(users_v1.router, prefix="/api/v1")
app.include_router(users_v2.router, prefix="/api/v2")
```

---

## 17. Common Pitfalls

| Pitfall | Fix |
|:--------|:----|
| Blocking calls inside `async def` routes | Use `def` for sync/blocking work, or `run_in_executor` |
| One huge `main.py` with all routes | Split into domain-based routers and services |
| Using Pydantic v1 syntax (`orm_mode`, `.dict()`) | Migrate to `ConfigDict(from_attributes=True)`, `model_dump()` |
| Not using `pool_pre_ping=True` | Stale DB connections cause random failures |
| Returning ORM objects directly | Always use `response_model` with Pydantic schemas |
| Hardcoded settings | Use `pydantic-settings` with `.env` files |
| No input validation in routes | Lean on Pydantic schemas + Zod-like Field constraints |
| Skipping Alembic | Manual schema changes are untrackable and dangerous |
| `@app.on_event("startup")` | Deprecated — use `lifespan` context manager |
| No error handling middleware | Unhandled exceptions leak server internals |

---

## 18. Recommended Stack (2025–2026)

| Layer | Tool |
|:------|:-----|
| Framework | FastAPI 0.115+ |
| Validation | Pydantic v2 + pydantic-settings |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Server | Uvicorn (ASGI) |
| Auth | python-jose (JWT) + passlib (bcrypt) |
| Testing | pytest + httpx + pytest-asyncio |
| Linting | Ruff (replaces flake8 + isort + black) |
| Dependency management | uv or poetry |
| Task queue | Celery + Redis (heavy) or BackgroundTasks (light) |
| Containerization | Docker with multi-stage builds |
