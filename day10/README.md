# Day 10 — FastAPI Testing, Docker and PostgreSQL

## 1. Project Overview

On Day 10 of my 30-Day Python Backend Development Roadmap, I developed and containerized an asynchronous REST API using FastAPI, PostgreSQL, SQLAlchemy, Docker, and Docker Compose.

The project focuses on reliable backend testing, database isolation, reusable test factories, container orchestration, and code coverage.

It builds on earlier asynchronous API development by introducing a more structured, production-oriented development workflow.

### Key Features

- Asynchronous FastAPI REST endpoints
- PostgreSQL-backed task management
- Full CRUD operations
- Cursor-based pagination
- Pydantic request validation
- Dockerized application environment
- PostgreSQL container with persistent storage
- Docker Compose service orchestration
- Automated asynchronous integration testing
- Database transaction rollback between tests
- Reusable test data factories
- Code coverage tooling

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Containerized application runtime |
| FastAPI | REST API development |
| PostgreSQL 18 | Relational database |
| SQLAlchemy Async | Asynchronous database ORM |
| asyncpg | PostgreSQL asynchronous driver |
| Pydantic | Request and response validation |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| WSL2 | Linux container development on Windows |
| uv | Dependency management |
| pytest | Automated testing |
| pytest-asyncio | Asynchronous tests |
| HTTPX | API integration testing |
| Psycopg | Synchronous test database setup |
| pytest-cov | Test coverage reporting |

## 3. Project Structure

```text
day10/
├── testing_docker_api/
│   ├── src/
│   │   └── testing_docker_api/
│   │       ├── api/
│   │       │   └── __init__.py
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── crud.py
│   │       ├── database.py
│   │       ├── models.py
│   │       └── schemas.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── factories.py
│   │   └── test_tasks.py
│   ├── Dockerfile
│   ├── compose.yaml
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── .gitignore
│   └── .python-version
└── README.md
```

## 4. Topics Covered

- Docker fundamentals
- Docker image creation
- Docker Compose
- Container networking
- PostgreSQL containerization
- Docker volumes and persistence
- Container health checks
- Asynchronous REST APIs
- SQLAlchemy database sessions
- Database transaction management
- Test fixtures and dependency overrides
- Reusable test factories
- Integration testing
- Test isolation and rollback
- Code coverage
- Dependency management using uv

## 5. Application Architecture

The application separates HTTP request handling, business operations, data validation, and database access.

### Main Components

**`main.py`**

Defines FastAPI endpoints, application lifespan management, and database dependency injection.

**`crud.py`**

Implements asynchronous task creation, retrieval, listing, updating, and deletion.

**`database.py`**

Configures the asynchronous SQLAlchemy engine, database session factory, and FastAPI database dependency.

**`models.py`**

Defines the PostgreSQL task model.

**`schemas.py`**

Defines Pydantic request, response, update, and pagination schemas.

**`tests/`**

Contains integration tests, reusable factories, and isolated database fixtures.

## 6. Docker Architecture

The application uses two Docker Compose services.

### API Container

- Image: `day10-fastapi:latest`
- Internal port: `8000`
- Host binding: `127.0.0.1:8000`
- Framework: FastAPI
- ASGI server: Uvicorn

### PostgreSQL Container

- Image: `postgres:18`
- Database: `day10_tasks`
- Internal port: `5432`
- Host binding: `127.0.0.1:5433`
- Persistent volume: `postgres_data`

The API connects to PostgreSQL using the Compose service hostname `postgres`.

### Container Communication

```text
Client
   |
   v
127.0.0.1:8000
   |
   v
FastAPI Container
   |
   | SQLAlchemy + asyncpg
   v
postgres:5432
   |
   v
PostgreSQL 18
   |
   v
postgres_data Volume
```

Docker Compose waits for PostgreSQL to pass its health check before starting the API service.

## 7. REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks |
| GET | `/tasks/{task_id}` | Retrieve a task |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Example: Create a Task

Request:

```http
POST /tasks
Content-Type: application/json

{
  "title": "Learn Docker",
  "description": "Practice Docker Compose"
}
```

Successful response: HTTP `201 Created`.

### Example: Update a Task

```http
PATCH /tasks/1
Content-Type: application/json

{
  "title": "Learn PostgreSQL",
  "completed": true
}
```

### Example: Cursor Pagination

```http
GET /tasks?limit=2
```

The response includes:

- `items`
- `next_cursor`
- `has_more`

The implementation uses ascending task IDs and retrieves one additional record to determine whether another page exists.

## 8. PostgreSQL Database Model

The `tasks` table contains:

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `title` | String(100) | Task title |
| `description` | Text | Optional description |
| `completed` | Boolean | Completion status |
| `created_at` | Timestamp | Creation timestamp |

The project uses asynchronous SQLAlchemy sessions for database operations.

## 9. Installation and Setup

### Prerequisites

- Docker Desktop
- Docker Compose
- WSL2 on Windows
- Python 3.11+ for local development
- uv

### Open the Project

From `day10`:

```powershell
cd testing_docker_api
```

### Configure Environment Variables

Create a local `.env` file containing:

```dotenv
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
```

Use your own credentials. Never commit `.env` to GitHub.

### Build the Docker Image

The Compose file references an existing image rather than defining a build context.

Build it first:

```powershell
docker build -t day10-fastapi:latest .
```

### Start the Containers

```powershell
docker compose up -d
```

### Check Container Status

```powershell
docker compose ps
```

### View API Logs

```powershell
docker compose logs -f api
```

### Stop the Containers

```powershell
docker compose down
```

The named database volume remains available unless explicitly removed.

## 10. API Documentation

Once the application is running, open:

```text
http://127.0.0.1:8000/docs
```

FastAPI also provides:

- `/redoc`
- `/openapi.json`

## 11. Automated Testing Architecture

The project uses pytest, pytest-asyncio, and HTTPX for asynchronous API integration tests.

### `conftest.py`

Defines reusable fixtures for:

- Test database preparation
- Asynchronous test engine
- Isolated database sessions
- HTTPX asynchronous test client
- FastAPI dependency overrides

### `factories.py`

Defines `make_task_payload()` to generate valid task creation data.

The factory supports optional titles and descriptions and generates unique default titles using a counter.

### `test_tasks.py`

Contains 13 automated test cases.

## 12. Test Cases

| Test | Purpose |
|---|---|
| Create task | Verify successful creation |
| Test isolation | Verify an empty task collection |
| Retrieve task | Verify retrieval by ID |
| Update task | Verify partial update |
| Delete task | Verify deletion and subsequent 404 |
| Missing task | Verify 404 response |
| Invalid title | Verify validation error |
| Invalid pagination limit | Verify limit constraints |
| Cursor pagination | Verify paginated retrieval |
| Update missing task | Verify 404 response |
| Delete missing task | Verify 404 response |
| Empty task list | Verify empty pagination response |
| Invalid cursor | Verify cursor validation |

**Total: 13 test cases defined in the reviewed source code.**

## 13. Test Database Isolation

The testing architecture uses a dedicated PostgreSQL database named:

```text
day10_tasks_test
```

The test configuration checks the connected database name before creating tables.

Each test receives a database session associated with an outer transaction.

SQLAlchemy's `join_transaction_mode="create_savepoint"` allows application-level commits to occur within savepoints.

At the end of the test, the outer transaction is rolled back.

### Why This Matters

Database isolation helps ensure that:

- Test data does not leak between tests.
- Tests remain repeatable.
- Application commits do not permanently modify test records.
- Development data remains separate from test operations.

The database preparation fixture creates missing tables but does not drop the existing schema.

## 14. Running Tests

Configure a separate PostgreSQL test database.

Example local `.env` values:

```dotenv
DATABASE_URL=postgresql+asyncpg://your_user:your_password@127.0.0.1:5433/day10_tasks
TEST_DATABASE_URL=postgresql+asyncpg://your_user:your_password@127.0.0.1:5433/day10_tasks_test
```

The test database must exist before running the test suite.

The provided Docker Compose configuration creates `day10_tasks`, not `day10_tasks_test` automatically.

### Install Development Dependencies

```powershell
uv sync
```

### Run Tests

```powershell
uv run python -m pytest tests/ -v
```

The latest test execution result has not been reverified during this README update.

## 15. Code Coverage

pytest-cov is included in the development dependencies.

Run:

```powershell
uv run python -m pytest tests/ --cov=testing_docker_api --cov-report=term-missing
```

To generate an HTML report:

```powershell
uv run python -m pytest tests/ --cov=testing_docker_api --cov-report=html
```

The HTML report is generated in `htmlcov/`.

No specific coverage percentage is claimed without a verified report.

## 16. Git Hygiene

The project `.gitignore` excludes:

- `.env` files
- `.venv/`
- Python cache files
- pytest cache
- Coverage databases
- HTML coverage reports

The generated `.coverage_debug` file is covered by the `.coverage.*` ignore rule.

The generated `coverage-debug.json` file is not explicitly covered by the shown `.gitignore` rules and should not be committed unintentionally.

## 17. Troubleshooting

### Docker Cannot Connect to PostgreSQL

Check:

```powershell
docker compose ps
docker compose logs postgres
```

Verify that PostgreSQL is healthy and that the database credentials match.

### API Container Fails to Start

Check:

```powershell
docker compose logs api
```

Verify the image was built and the required environment variables are configured.

### Port Already in Use

The API uses host port `8000`, while PostgreSQL uses host port `5433`.

Check for existing services using those ports.

### Tests Cannot Connect to the Database

Verify:

- PostgreSQL is running.
- `TEST_DATABASE_URL` is configured.
- The test database exists.
- The database name is exactly `day10_tasks_test`.
- The configured database user has the required permissions.

## 18. Role and Importance of the Project

### Containerization

Docker packages an application and its runtime dependencies into a reproducible environment.

### Service Orchestration

Docker Compose coordinates multiple services and their dependencies.

### Database Reliability

PostgreSQL provides persistent storage, while Docker volumes preserve data across container restarts.

### Automated Testing

Integration tests verify real interactions between the API and database.

### Test Isolation

Transactional rollback improves test repeatability and reduces unwanted side effects.

### Code Coverage

Coverage reporting identifies code paths that automated tests have not executed.

### Professional Project Organization

A structured `src/` layout, dependency lockfile, tests, and container configuration improve maintainability.

## 19. Real-World Applications

These techniques are useful for:

- Containerized REST APIs
- Backend microservices
- Database-backed business applications
- Development and testing environments
- Automated integration testing workflows
- Continuous integration pipelines

## 20. Known Limitations

- The application creates missing database tables at startup instead of using versioned migrations.
- Authentication and authorization are not implemented in the reviewed API.
- The Dockerfile uses a development-oriented dependency installation workflow.
- The Compose configuration does not automatically provision the separate test database.
- Production deployment, monitoring, and hardened security configuration are outside the verified implementation.

## 21. Learning Outcomes

By completing Day 10, I gained practical experience with:

- Docker images and containers
- Docker Compose
- WSL2-based development
- Container networking
- PostgreSQL persistence
- Asynchronous database operations
- FastAPI integration testing
- pytest fixtures
- Database transaction isolation
- Reusable test factories
- Code coverage analysis
- Professional backend project structure

## 22. Day 10 Deliverables

- Containerized FastAPI application
- PostgreSQL 18 container
- Docker Compose configuration
- Persistent database volume
- Asynchronous CRUD API
- Cursor-based pagination
- Dedicated database testing fixtures
- Reusable task factory
- 13 automated integration tests
- Code coverage configuration
- Professional project documentation

---

**Roadmap:** 30-Day Python Backend Development  
**Day:** 10  
**Project:** FastAPI Testing, Docker and PostgreSQL  
**Status:** Implementation documented; latest test execution not reverified