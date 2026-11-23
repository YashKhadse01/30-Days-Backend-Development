# Day 09 — Asynchronous Task Management API with PostgreSQL

## 1. Project Overview

On Day 09 of my 30-Day Python Backend Development Roadmap, I developed an asynchronous RESTful Task Management API using **FastAPI, SQLAlchemy Async, asyncpg, and PostgreSQL**.

The project demonstrates how asynchronous database operations can be integrated with REST APIs to support persistent task management, data validation, cursor-based pagination, and automated integration testing.

### Key Features

- Asynchronous REST API endpoints
- PostgreSQL database persistence
- Full task CRUD operations
- SQLAlchemy asynchronous ORM
- Pydantic request and response validation
- Cursor-based pagination
- Dependency-injected database sessions
- Automated PostgreSQL integration tests
- Dedicated test database safeguards
- Automatic OpenAPI documentation

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend development |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy Async | Asynchronous ORM and database operations |
| asyncpg | Asynchronous PostgreSQL driver |
| Pydantic | Data validation and serialization |
| pydantic-settings | Environment-based configuration |
| pytest | Automated testing |
| pytest-asyncio | Asynchronous test execution |
| HTTPX | Asynchronous API testing |
| uv | Dependency management |
| Git and GitHub | Version control |

## 3. Project Structure

```text
day09/
├── async_task_api/
│   ├── app/
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── src/
│   │       └── app/
│   │           └── __init__.py
│   ├── tests/
│   │   ├── test_tasks.py
│   │   └── src/
│   │       └── test__init__.py
│   ├── .env.example
│   ├── .gitignore
│   ├── check_db.py
│   ├── create_tables.py
│   ├── pyproject.toml
│   └── uv.lock
└── README.md
```

## 4. Topics Covered

- Python asynchronous programming
- FastAPI asynchronous route handlers
- PostgreSQL database integration
- SQLAlchemy asynchronous sessions
- Database dependency injection
- ORM model development
- Pydantic schema validation
- RESTful CRUD operations
- Cursor-based pagination
- HTTP exception handling
- Application lifespan management
- Asynchronous integration testing
- Test database isolation

## 5. Application Architecture

The project separates backend responsibilities into dedicated modules.

### `app/main.py`

Defines FastAPI endpoints, dependency injection, HTTP responses, and application lifespan behavior.

### `app/database.py`

Manages:

- Environment-based database configuration
- Asynchronous SQLAlchemy engine
- Async session factory
- Database session dependency
- Connection health checking through `pool_pre_ping`

### `app/models.py`

Defines the SQLAlchemy ORM model for the PostgreSQL `tasks` table.

### `app/schemas.py`

Defines Pydantic models for task creation, updates, responses, and paginated results.

### `app/crud.py`

Implements asynchronous database operations for creating, retrieving, updating, deleting, and listing tasks.

### `tests/test_tasks.py`

Contains asynchronous API integration tests using HTTPX, pytest-asyncio, and a dedicated PostgreSQL test database.

## 6. Database Design

The project uses a PostgreSQL table named `tasks`.

| Column | Type | Description |
|---|---|---|
| `id` | Integer | Auto-incrementing primary key |
| `title` | String(100) | Required task title |
| `description` | Text | Optional task description |
| `completed` | Boolean | Task completion status |
| `created_at` | Timestamp with timezone | Task creation timestamp |

The ORM model defines `completed` as `False` by default and uses the database server's current timestamp for `created_at`.

## 7. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | List tasks with cursor pagination |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PATCH | `/tasks/{task_id}` | Partially update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Create a Task

Request:

```http
POST /tasks
Content-Type: application/json

{
  "title": "Learn asynchronous Python",
  "description": "Practice FastAPI with PostgreSQL"
}
```

A successful request returns HTTP `201 Created` with the persisted task, including its ID, completion status, and creation timestamp.

### Retrieve a Task

```http
GET /tasks/1
```

Returns the requested task or HTTP `404` when it does not exist.

### Update a Task

```http
PATCH /tasks/1
Content-Type: application/json

{
  "title": "Learn SQLAlchemy Async",
  "completed": true
}
```

The endpoint supports partial updates.

### Delete a Task

```http
DELETE /tasks/1
```

A successful deletion returns HTTP `204 No Content`.

## 8. Cursor-Based Pagination

The task listing endpoint uses the task's numeric ID as a pagination cursor.

Example:

```http
GET /tasks?limit=2
```

The response includes:

```json
{
  "items": [],
  "next_cursor": null,
  "has_more": false
}
```

This example illustrates the response structure for an empty result set.

### Pagination Parameters

| Parameter | Default | Constraint |
|---|---|---|
| `cursor` | None | Integer, minimum 0 |
| `limit` | 10 | Integer between 1 and 100 |

The database query orders tasks by ascending ID and retrieves `limit + 1` records.

The additional record determines whether more results are available.

When another page exists, `next_cursor` contains the ID of the last returned task.

### Why Cursor Pagination Matters

Cursor pagination is useful for APIs that process large or changing datasets because it avoids repeatedly skipping earlier rows through large offsets.

## 9. Asynchronous Database Operations

The project uses `async def` endpoints with SQLAlchemy's `AsyncSession`.

Database operations are executed with `await`, including:

- `db.execute()`
- `db.commit()`
- `db.refresh()`
- `db.get()`
- `db.delete()`

Database sessions are supplied through FastAPI dependency injection.

This design separates HTTP request handling from database persistence logic.

## 10. Installation and Setup

### Prerequisites

- Python 3.11 or newer
- PostgreSQL
- uv package manager

### Open the Project Directory

From `day09`:

```powershell
cd async_task_api
```

### Install Dependencies

```powershell
uv sync
```

### Configure PostgreSQL

Create a PostgreSQL development database and a separate test database.

The integration tests specifically require the test database to be named:

```text
day9_tasks_test
```

### Configure Environment Variables

Create a `.env` file in the `async_task_api` directory.

Example:

```dotenv
DATABASE_URL=postgresql+asyncpg://your_user:your_password@127.0.0.1:5432/your_development_database
TEST_DATABASE_URL=postgresql+asyncpg://your_test_user:your_test_password@127.0.0.1:5432/day9_tasks_test
```

Replace the placeholders with your local PostgreSQL configuration.

Never commit actual database passwords or `.env` files.

### Verify Database Connectivity

```powershell
uv run python check_db.py
```

The script connects to PostgreSQL and prints the connected database name.

### Create Database Tables

```powershell
uv run python create_tables.py
```

The script creates missing tables using SQLAlchemy metadata.

The FastAPI application also creates missing tables during startup.

### Start the API

```powershell
uv run uvicorn app.main:app --reload
```

The development server is normally available at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI provides:

- `/docs` — Swagger UI
- `/redoc` — ReDoc
- `/openapi.json` — Generated OpenAPI schema

## 11. Automated Integration Testing

The project defines nine asynchronous integration tests.

| Test | Purpose |
|---|---|
| `test_health` | Verify health endpoint |
| `test_create_task` | Verify task creation |
| `test_get_task` | Verify task retrieval |
| `test_update_task` | Verify partial updates |
| `test_delete_task` | Verify deletion |
| `test_missing_task` | Verify missing-task response |
| `test_invalid_title` | Verify Pydantic validation |
| `test_cursor_pagination` | Verify pagination across three pages |
| `test_invalid_page_limit` | Verify pagination limit validation |

### Run Tests

From the `async_task_api` directory:

```powershell
uv run python -m pytest tests/ -v
```

**Test suite:** 9 integration tests defined in the reviewed source code.

The latest execution result has not been reverified during this documentation update.

## 12. Test Database Safety

The integration tests include safeguards to prevent accidental modification of the development database.

Before executing database setup operations, the test fixture:

1. Requires `TEST_DATABASE_URL`.
2. Checks that the URL uses the `postgresql+asyncpg` scheme.
3. Requires the database path to be `/day9_tasks_test`.
4. Connects to PostgreSQL and verifies the actual database name.
5. Refuses to modify a database with a different name.

**Important:** The test fixture drops and recreates all tables registered in the project's SQLAlchemy metadata within the dedicated test database. Never point `TEST_DATABASE_URL` to a database containing valuable data.

The tests override FastAPI's database dependency so API requests use the test database rather than the development database.

## 13. Application Lifespan

The FastAPI application uses an asynchronous lifespan context manager.

During startup, it creates missing database tables.

During shutdown, it disposes of the database engine.

This demonstrates application resource initialization and cleanup.

For production systems, versioned database migrations such as Alembic are generally preferable to automatically creating tables on startup.

## 14. Role and Importance of the Project

This project demonstrates several important backend engineering concepts.

### Asynchronous Request Handling

Asynchronous operations allow applications to handle database I/O without blocking the event loop while awaiting results.

### Persistent Data Storage

PostgreSQL provides durable relational storage beyond the lifetime of the application process.

### Separation of Responsibilities

Dedicated API, database, model, schema, and CRUD modules improve maintainability.

### Pagination

Cursor-based pagination helps APIs retrieve large collections in manageable batches.

### Database Safety

Separate test databases and validation checks reduce the risk of destructive tests affecting development data.

### Automated Testing

Integration tests verify interactions between the API, database, validation layer, and persistence logic.

## 15. Real-World Applications

The concepts demonstrated in this project can support:

- Task management platforms
- Workflow management systems
- Project tracking applications
- Internal business APIs
- Database-backed administrative services
- Backend services requiring paginated data retrieval

## 16. Known Limitations

- Authentication and authorization are not implemented in the reviewed endpoints.
- Database schema migrations are not version-controlled through Alembic.
- Pagination uses numeric task IDs as cursors.
- No background task queue is implemented in the reviewed code.
- Production deployment, monitoring, and operational security configuration are outside the verified implementation.

## 17. Learning Outcomes

By completing Day 09, I gained practical experience with:

- Asynchronous FastAPI development
- PostgreSQL integration using asyncpg
- SQLAlchemy AsyncSession
- Database dependency injection
- Persistent CRUD operations
- Pydantic request validation
- Cursor-based pagination
- Application lifespan management
- Asynchronous integration testing
- Dedicated test database safety

## 18. Day 09 Deliverables

- Asynchronous FastAPI Task Management API
- PostgreSQL database integration
- SQLAlchemy ORM models
- CRUD service layer
- Pydantic request and response schemas
- Cursor-based pagination
- Database connectivity utility
- Database table creation utility
- Nine automated integration tests
- Professional Day 09 documentation

---

**Roadmap:** 30-Day Python Backend Development  
**Day:** 09  
**Project:** Async Task Management API with PostgreSQL  
**Status:** Implementation documented; latest tests not rerun during this README update