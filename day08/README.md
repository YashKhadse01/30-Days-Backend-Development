# Day 08 — FastAPI Fundamentals and API Design

## 1. Project Overview

On Day 08 of my 30-Day Python Backend Development Roadmap, I explored FastAPI fundamentals, REST API design, Pydantic validation, modular application architecture, OpenAPI documentation, and automated API testing.

The day's implementation consists of two applications:

1. **TaskFlow API:** A modular, design-first FastAPI application demonstrating reusable routers, response schemas, and OpenAPI documentation.
2. **Task Management Practice API:** An in-memory task management application demonstrating REST endpoints, path parameters, query parameters, data validation, and error handling.

The objective was to understand how modern Python web frameworks simplify API development while encouraging maintainable application design.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend programming |
| FastAPI | REST API development |
| Pydantic | Request and response validation |
| Uvicorn | ASGI development server |
| pytest | Automated testing |
| HTTPX / TestClient | HTTP endpoint testing |
| OpenAPI | API specification |
| Swagger UI | Interactive API documentation |
| uv | Dependency management |
| Git and GitHub | Version control |

## 3. Project Structure

```text
day08/
├── fastapi_project/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       └── health.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── health.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── docs/
│   │   ├── api_design.md
│   │   └── openapi.yaml
│   ├── tests/
│   │   └── test_health.py
│   ├── models.py
│   ├── practice_api.py
│   ├── test_app.py
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .python-version
└── README.md
```

## 4. Topics Covered

- FastAPI application initialization
- RESTful API design
- HTTP GET and POST methods
- Dynamic path parameters
- Query parameter validation
- Pydantic request and response models
- Reusable API routers
- HTTP status codes
- Exception handling
- OpenAPI schema generation
- Swagger UI documentation
- Automated endpoint testing
- Modular project organization

## 5. TaskFlow API — Modular Application

The TaskFlow application demonstrates a structured approach to building FastAPI services.

### Application Initialization

`app/main.py` initializes the application with:

- Title: TaskFlow API
- Version: 1.0.0
- Description: Design-first FastAPI project skeleton

It registers the health router using `app.include_router()`.

### Health Router

The health endpoint is implemented in:

`app/api/routes/health.py`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Return application health status |

Example response:

```json
{
  "status": "healthy"
}
```

### Response Validation

The health response uses a Pydantic model:

```python
class HealthResponse(BaseModel):
    status: str
```

This provides a defined response structure and contributes to generated API documentation.

## 6. Task Management Practice API

The practice application demonstrates API development using an in-memory task collection.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/greet/{name}` | Dynamic greeting |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task |
| GET | `/search` | Filter tasks by keyword or priority |

### Task Creation

Example request:

```http
POST /tasks
Content-Type: application/json

{
  "title": "Learn FastAPI",
  "description": "Practice REST API development",
  "priority": 3
}
```

Example successful response:

```json
{
  "title": "Learn FastAPI",
  "description": "Practice REST API development",
  "priority": 3,
  "id": 1,
  "completed": false
}
```

HTTP status: `201 Created`.

### Task Search

The search endpoint supports:

- `keyword`: Optional case-insensitive title search, minimum two characters
- `priority`: Optional priority filter between 1 and 5

Example:

```http
GET /search?keyword=Python&priority=3
```

Both filters can be combined.

### Task Retrieval

Tasks can be retrieved individually using their numeric ID.

If a task does not exist, the API returns HTTP `404`.

## 7. Pydantic Data Validation

The practice API defines two Pydantic models.

### TaskCreate

Validates incoming task data:

- `title`: String, 3–100 characters
- `description`: Optional string
- `priority`: Integer between 1 and 5, defaulting to 1

### TaskResponse

Extends `TaskCreate` with:

- `id`: Integer task identifier
- `completed`: Boolean, defaulting to `False`

Pydantic automatically validates incoming requests and provides structured validation errors.

Invalid input can produce HTTP `422 Unprocessable Entity`.

## 8. OpenAPI and Swagger UI

FastAPI automatically generates an OpenAPI schema from registered endpoints and models.

The project also contains dedicated API design documents:

- `docs/api_design.md`
- `docs/openapi.yaml`

These files are included as project documentation artifacts. Their contents have not been reviewed as part of this README update.

FastAPI's generated documentation is available at:

```text
/docs
/redoc
/openapi.json
```

## 9. Installation and Setup

### Prerequisites

- Python 3.11 or newer
- uv package manager

### Open the Project

From the `day08` directory:

```powershell
cd fastapi_project
```

### Install Dependencies

```powershell
uv sync
```

### Run TaskFlow API

```powershell
uv run uvicorn app.main:app --reload
```

### Run the Practice API

In a separate terminal, or after stopping TaskFlow:

```powershell
uv run uvicorn practice_api:app --reload
```

By default, Uvicorn serves the application at:

```text
http://127.0.0.1:8000
```

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

## 10. Automated Testing

The project includes separate tests for the modular application and practice API.

### TaskFlow Tests

`tests/test_health.py` contains three tests covering:

- Successful health endpoint response
- JSON response structure
- OpenAPI schema availability

### Practice API Tests

`test_app.py` contains seven tests covering:

- Health endpoint
- Task creation
- Task listing
- Priority-based searching
- Invalid priority validation
- Invalid task title validation
- Missing task handling

### Run All Tests

From the `fastapi_project` directory:

```powershell
uv run python -m pytest tests/ test_app.py -v
```

**Test suite:** 10 tests defined in the reviewed source files.

The latest passing-test count has not been independently verified during this documentation update.

## 11. Architecture and Design

The project demonstrates two approaches to organizing FastAPI applications.

**Modular design:** TaskFlow separates API routes, schemas, and application initialization into dedicated modules.

**Single-file practice design:** The task management application places its route handlers in `practice_api.py`, making it easier to explore core FastAPI concepts.

Both approaches help demonstrate how API complexity influences application structure.

## 12. Role and Importance of the Project

This project introduces essential skills required for professional Python backend development.

### API Design

REST endpoints provide a structured way for frontend applications and other services to communicate with a backend.

### Data Validation

Pydantic ensures that incoming request data follows expected constraints, reducing invalid application state.

### Modular Architecture

Separating routers, schemas, and application configuration improves code organization and maintainability.

### API Documentation

OpenAPI and Swagger UI help developers understand, explore, and test available endpoints.

### Automated Testing

Endpoint tests help identify regressions and verify expected API behavior.

## 13. Limitations

- The practice application stores tasks in memory, so data is lost when the process restarts.
- No database persistence is implemented in the reviewed practice API.
- Task update and deletion endpoints are not implemented in the supplied code.
- The practice API contains a duplicate `/search` route declaration.
- Authentication and authorization are not implemented in the reviewed endpoints.
- The modular TaskFlow application currently exposes the health endpoint in the reviewed code.

## 14. Learning Outcomes

By completing Day 08, I gained practical experience with:

- Creating FastAPI applications
- Designing REST API endpoints
- Using path and query parameters
- Implementing Pydantic validation
- Organizing routes into reusable modules
- Generating OpenAPI documentation
- Writing automated endpoint tests
- Managing dependencies using uv
- Understanding the importance of maintainable API architecture

## 15. Day 08 Deliverables

- Modular TaskFlow FastAPI application
- Health endpoint and response schema
- Task management practice API
- Task creation and retrieval
- Keyword and priority search
- Pydantic request validation
- OpenAPI and API design documentation files
- Automated API test suite
- Professional project documentation

---

**Roadmap:** 30-Day Python Backend Development  
**Day:** 08  
**Project:** FastAPI Fundamentals and API Design  
**Status:** Implementation documented; latest test execution not reverified