import asyncio
import os

import asyncpg
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

TEST_DB = "student_management_test"
ADMIN_DSN = os.getenv(
    "TEST_ADMIN_DSN", "postgresql://student_user:student_password@localhost:5432/postgres"
)
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    f"postgresql+asyncpg://student_user:student_password@localhost:5432/{TEST_DB}",
)

# Must be set before the app is imported so its engine never points at the dev database.
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from backend.api.main import app  # noqa: E402
from backend.database import Base, get_db  # noqa: E402
from backend.models import Student  # noqa: E402

SEED = [
    {"id": 1, "name": "Rahul Sharma", "age": 21, "course": "AI", "email": "rahul@gmail.com"},
    {"id": 2, "name": "Priya Patel", "age": 22, "course": "Data Science", "email": "priya@gmail.com"},
    {"id": 3, "name": "Aman Verma", "age": 20, "course": "Web Development", "email": "aman@gmail.com"},
    {"id": 4, "name": "Sneha Reddy", "age": 23, "course": "Cyber Security", "email": "sneha@gmail.com"},
]

# NullPool: TestClient and asyncio.run use different event loops, and pooled asyncpg
# connections can't be shared across loops.
engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def _create_database():
    conn = await asyncpg.connect(ADMIN_DSN)
    try:
        if not await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", TEST_DB):
            await conn.execute(f'CREATE DATABASE "{TEST_DB}"')
    finally:
        await conn.close()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def _reset(rows):
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE students"))
    async with SessionLocal() as session:
        session.add_all(Student(**r) for r in rows)
        await session.commit()


async def _override_get_db():
    async with SessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def test_database():
    asyncio.run(_create_database())
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def seeded_students():
    asyncio.run(_reset(SEED))


@pytest.fixture
def empty_db():
    asyncio.run(_reset([]))


@pytest.fixture
def client():
    return TestClient(app)
