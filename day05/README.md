# Day 05 - HTTP Fundamentals and Raw HTTP JSON Server

## Overview

Day 05 of my 30-Day Backend Development roadmap focuses on understanding how HTTP communication works internally.

The main project is a **Raw HTTP JSON Server**, developed using Python's built-in `socket` module without Flask, Django, FastAPI, or another web framework.

The application demonstrates how a backend server accepts TCP connections, processes HTTP requests, routes endpoints, validates JSON input, and constructs HTTP responses.

## Learning Objectives

- Understand TCP/IP networking fundamentals.
- Learn the HTTP request-response lifecycle.
- Understand HTTP methods and status codes.
- Create TCP clients and servers using Python sockets.
- Parse HTTP request lines, headers, and bodies.
- Build JSON responses manually.
- Implement REST-style API routing.
- Validate incoming JSON data.
- Handle malformed requests and socket timeouts.
- Write automated tests for HTTP server functionality.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core programming language |
| socket | TCP network communication |
| json | JSON serialization and deserialization |
| urllib.parse | URL path extraction |
| pytest | Automated testing |
| pytest-cov | Code coverage measurement |
| curl | Manual HTTP request testing |

## Project Structure

```text
day05/
├── README.md
├── practice/
│   ├── tcp_client.py
│   ├── tcp_server.py
│   ├── http_parser.py
│   ├── http_routes.py
│   └── raw_http.py
└── raw_http_server/
    ├── README.md
    ├── app.py
    ├── server.py
    ├── test_app.py
    ├── test_server.py
    └── test_api_manual.py
```

## Main Project - Raw HTTP JSON Server

The application provides a small REST-style API for managing users.

It uses an in-memory Python list to store user records.

### API Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/` | Welcome message | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/users` | Retrieve users | 200 |
| GET | `/users/{id}` | Retrieve a specific user | 200 |
| POST | `/users` | Create a user | 201 |

The server also returns appropriate error responses for invalid requests, unsupported methods, and missing resources.

## Application Architecture

```text
HTTP Client
    |
    v
TCP Socket Connection
    |
    v
server.py
    |
    +-- Accept connection
    +-- Read HTTP request
    +-- Parse headers and body
    +-- Validate request format
    |
    v
app.py
    |
    +-- Match route
    +-- Validate JSON
    +-- Execute application logic
    |
    v
server.py
    |
    +-- Serialize JSON
    +-- Generate HTTP status line
    +-- Add response headers
    |
    v
HTTP Response
```

## Core Implementation

### 1. TCP Socket Server

The server uses `socket.AF_INET` and `socket.SOCK_STREAM` to create an IPv4 TCP socket.

It binds to:

```text
127.0.0.1:8003
```

The server accepts incoming connections and processes them sequentially.

### 2. HTTP Request Parsing

The `read_request()` function:

- Reads the request from the socket.
- Separates HTTP headers from the body.
- Validates the request line.
- Accepts HTTP/1.0 and HTTP/1.1.
- Parses headers.
- Rejects duplicate headers.
- Rejects unsupported transfer encoding.
- Validates `Content-Length`.
- Reads the expected request body.

The implementation limits headers to 65,536 bytes and request bodies to 1,000,000 bytes.

### 3. API Routing

The `handle_request()` function handles application-level routing.

It returns a tuple containing:

```python
(status_code, response_data)
```

The function supports retrieving users, creating users, and returning error responses.

### 4. JSON Validation

When creating a user, the application:

1. Decodes the request body as UTF-8.
2. Parses the JSON.
3. Confirms the JSON value is an object.
4. Validates the `name` field.
5. Creates a new user with an incremented ID.
6. Returns HTTP 201.

### 5. HTTP Response Construction

The `build_response()` function generates:

- HTTP status line.
- Content-Type header.
- Content-Length header.
- Connection header.
- UTF-8 encoded JSON body.

### 6. Error Handling

The implementation handles malformed requests, invalid JSON, unsupported methods, missing endpoints, and socket timeouts.

## Installation and Execution

Requirements: Python 3.11 or later.

From the repository root:

```powershell
cd day05\raw_http_server
```

Start the server:

```powershell
python server.py
```

Expected startup address:

```text
http://127.0.0.1:8003
```

Stop the server using `Ctrl+C`.

## Manual API Testing

Open a second terminal while the server is running.

### Health Check

```powershell
curl.exe -i http://127.0.0.1:8003/health
```

### Retrieve Users

```powershell
curl.exe -i http://127.0.0.1:8003/users
```

### Retrieve a Specific User

```powershell
curl.exe -i http://127.0.0.1:8003/users/1
```

### Create a User

Create a UTF-8 file named `request.json` containing:

```json
{
  "name": "Charlie"
}
```

Send the request:

```powershell
curl.exe -i -X POST http://127.0.0.1:8003/users -H "Content-Type: application/json" --data-binary "@request.json"
```

A successful request returns HTTP 201.

## Automated Testing

Install test dependencies in your selected Python environment:

```powershell
python -m pip install pytest pytest-cov
```

Run tests:

```powershell
python -m pytest -v
```

Run coverage:

```powershell
python -m pytest -v --cov=app --cov=server --cov-report=term-missing
```

### Recorded Test Results

The existing project README reports:

| Metric | Result |
|---|---|
| Automated tests | 36 passed |
| `app.py` coverage | 100% |
| `server.py` coverage | 66% |
| Combined coverage | 77% |

These figures are recorded results from the existing project documentation.

## HTTP Status Codes Used

| Status | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 405 | Method Not Allowed |

## Real-World Applications

- Understanding how backend frameworks process HTTP requests.
- Learning low-level API communication.
- Debugging network and HTTP protocol issues.
- Understanding request validation and response construction.
- Building educational network services.
- Preparing for backend development interviews.

## Current Limitations

- Processes one connection at a time.
- Uses in-memory data storage.
- Does not implement HTTPS.
- Does not provide authentication or authorization.
- Does not support the full HTTP specification.
- Is not suitable for public production deployment.

## Future Improvements

- Add concurrent request handling.
- Integrate persistent database storage.
- Improve HTTP protocol compliance.
- Introduce structured logging.
- Add authentication and authorization.
- Explore production-ready web frameworks.

## Key Takeaways

Day 05 helped me understand how backend HTTP servers operate below the framework level.

By implementing request parsing, API routing, JSON validation, and HTTP response generation manually, I developed a stronger foundation for working with FastAPI, Django, and other backend technologies.

---

**Roadmap:** 30 Days of Backend Development  
**Day:** 05  
**Project:** Raw HTTP JSON Server  
**Status:** Completed - 36 passing tests reported in the existing project README.