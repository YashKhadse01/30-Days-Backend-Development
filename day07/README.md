# Day 07 — Building a Mini Web Framework in Python

## Project Overview

On Day 07 of my 30-Day Python Backend Development Roadmap, I built a lightweight web framework from scratch using Python's standard library.

The project demonstrates how web frameworks handle HTTP requests, register routes, execute endpoint functions, and generate JSON responses.

A RESTful To-Do API was developed on top of the custom framework to demonstrate CRUD operations.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core development |
| `http.server` | HTTP server implementation |
| `dataclasses` | Request and response models |
| `re` | Dynamic URL matching |
| `json` | JSON parsing and serialization |
| pytest | Automated testing |
| uv | Python environment and dependency execution |
| Git and GitHub | Version control |

## Topics Covered

- HTTP request-response lifecycle
- Custom request and response objects
- Route decorators
- Dynamic URL parameters
- REST API fundamentals
- CRUD operations
- JSON validation and error handling
- HTTP status codes
- Automated testing

## Project Structure

```text
day07/
├── mini_framework/
│   ├── app.py
│   ├── main.py
│   ├── server.py
│   └── test_app.py
├── practice/
│   ├── dynamic_router.py
│   ├── framework_basics.py
│   ├── request_response.py
│   └── route_decorators.py
└── README.md
```

## Framework Architecture

The framework is organized into three primary components.

### Request and Response Layer

`app.py` defines the `Request` and `Response` dataclasses.

The `Request` class represents incoming HTTP requests, including the method, URL path, headers, and body.

The `Response` class represents JSON response data and an HTTP status code.

### Routing and Dispatch Layer

`MiniApp` provides route registration decorators:

- `@app.get()`
- `@app.post()`
- `@app.put()`
- `@app.delete()`

The dispatcher matches incoming requests against registered routes, extracts numeric dynamic URL parameters, and executes the corresponding handler.

### HTTP Server Layer

`server.py` uses Python's `HTTPServer` and `BaseHTTPRequestHandler`.

The server translates HTTP requests into framework `Request` objects and sends the resulting JSON responses to clients.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| GET | `/todos` | Retrieve all To-Dos |
| GET | `/todos/{todo_id}` | Retrieve one To-Do |
| POST | `/todos` | Create a To-Do |
| PUT | `/todos/{todo_id}` | Update a To-Do |
| DELETE | `/todos/{todo_id}` | Delete a To-Do |

### Example: Create a To-Do

Request:

```http
POST /todos
Content-Type: application/json

{
  "title": "Learn Python"
}
```

Successful response:

```json
{
  "todo": {
    "id": 1,
    "title": "Learn Python",
    "completed": false
  }
}
```

HTTP status: `201 Created`.

## How to Run

### Prerequisites

- Python 3.11 or later
- uv for running the test suite

### Start the HTTP Server

From the `day07` directory:

```powershell
cd mini_framework
python server.py
```

The application runs at:

```text
http://127.0.0.1:8007
```

Visit:

```text
http://127.0.0.1:8007/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

### Run Automated Tests

From `mini_framework`:

```powershell
uv run --with pytest python -m pytest test_app.py -v
```

The supplied test file covers successful CRUD operations, validation errors, missing resources, routing failures, and JSON serialization.

## Input Validation and Error Handling

The application validates To-Do titles and completion values.

Examples include:

- Rejecting missing or empty titles
- Rejecting non-string titles
- Rejecting invalid completion values
- Rejecting JSON arrays where objects are required
- Returning `404` for unknown routes or missing To-Dos
- Returning `400` for malformed JSON

## Testing

The test suite uses pytest fixtures to reset in-memory application data before each test.

Test categories include:

- Health endpoint
- Listing To-Dos
- Creating To-Dos
- Retrieving To-Dos
- Updating To-Dos
- Deleting To-Dos
- Dynamic routing
- HTTP method matching
- Invalid JSON handling
- Response serialization

The previously recorded Day 07 testing milestone was **23 passing tests with 100% statement coverage for the framework and API modules**. These results are historical and have not been rerun during this README update.

## Role and Importance of the Project

Building a framework from scratch helps explain what established web frameworks do internally.

The project demonstrates:

- How an HTTP server receives requests
- How route decorators register endpoint handlers
- How URLs are matched to functions
- How request data is validated
- How structured JSON responses are generated
- How automated tests verify API behavior

These concepts form a foundation for understanding FastAPI, Flask, Django, and other backend frameworks.

## Limitations

This is an educational framework rather than a production-ready web server.

- To-Do data is stored in memory and disappears when the process stops.
- No database integration is included.
- Authentication and authorization are not implemented.
- Dynamic route parameters are limited to numeric values.
- The framework does not provide production-grade middleware, concurrency handling, or security protections.

## Learning Outcomes

By completing Day 07, I gained practical experience with HTTP fundamentals, framework architecture, route decorators, dynamic routing, CRUD API design, input validation, and automated testing.

## Day 07 Deliverables

- Custom Python mini web framework
- HTTP server
- RESTful To-Do CRUD API
- Dynamic route matching
- Request and response abstractions
- Four practice scripts
- Automated test suite
- Project documentation

---

**Roadmap:** 30-Day Python Backend Development  
**Day:** 07  
**Project:** Custom Mini Web Framework and To-Do REST API