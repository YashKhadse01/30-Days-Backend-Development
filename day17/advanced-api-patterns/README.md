# Day 17 — Advanced API Patterns with FastAPI & Redis

A Python backend engineering project demonstrating **API key authentication, idempotency, Redis caching, HTTP ETags, and optimistic concurrency control**.

Part of my **30 Days of Backend Development** journey.

## Project Overview

Production APIs need mechanisms beyond basic CRUD operations to manage client authentication, prevent duplicate operations, reduce repeated data retrieval, and protect resources from conflicting updates.

This project explores four advanced API design patterns using FastAPI and Redis.

## Key Features

- Cryptographically generated API keys
- SHA-256 hashing of stored API keys
- Scope-based API authorization
- API key revocation and rotation
- Idempotency keys for item creation
- Duplicate request replay and payload conflict detection
- Redis cache-aside with time-to-live (TTL)
- Cache hit/miss response headers
- HTTP ETag generation using SHA-256
- Conditional GET requests using `If-None-Match`
- Optimistic concurrency using `If-Match`
- Cache invalidation after updates
- Automated unit and integration tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend development |
| FastAPI | REST API framework |
| Redis | Response data caching |
| redis-py (asyncio) | Asynchronous Redis access |
| Uvicorn | ASGI server |
| Pydantic | Request validation |
| python-dotenv | Environment configuration |
| pytest | Automated testing |
| pytest-asyncio | Async testing |
| HTTPX | API integration testing |
| fakeredis | Redis testing |
| pytest-cov | Coverage reporting |
| uv | Dependency management |

## Project Structure

```text
advanced-api-patterns/
├── pyproject.toml
├── README.md
├── src/
│   ├── advanced_api/
│   │   ├── main.py
│   │   ├── api_keys.py
│   │   ├── cache.py
│   │   ├── etags.py
│   │   └── idempotency.py
│   └── advanced_api_patterns/
│       └── __init__.py
└── tests/
    ├── test_api_integration.py
    ├── test_api_keys.py
    ├── test_cache.py
    ├── test_cache_integration.py
    ├── test_etags.py
    ├── test_etag_integration.py
    └── test_idempotency.py
```

## Architecture

```text
                  API Client
                      |
                      v
                FastAPI Server
                      |
             API Key Validation
                      |
             Permission Checking
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
     Idempotency    Redis       ETags
       Manager      Cache       Manager
          |           |           |
          v           v           v
     Duplicate     Cache Hit/   Conditional
     Prevention    Miss Logic    Requests
          |           |           |
          +-----------+-----------+
                      |
                      v
              In-Memory Items
```

The application uses Redis for caching. API keys, idempotency records, and item data are stored in memory for demonstration purposes.

## Installation and Setup

### 1. Navigate to the project

From the repository root:

```powershell
cd day17\advanced-api-patterns
```

### 2. Install dependencies

Ensure Python 3.11+ and `uv` are installed.

```powershell
uv sync --group dev
```

### 3. Start Redis

The application defaults to Redis on port **6380**, rather than the standard port 6379.

Using Docker:

```powershell
docker run -d --name day17-redis -p 6380:6379 redis:7-alpine
```

If the container already exists and is stopped:

```powershell
docker start day17-redis
```

Verify connectivity:

```powershell
docker exec day17-redis redis-cli ping
```

Expected response:

```text
PONG
```

### 4. Configure the environment

The application reads the `REDIS_URL` environment variable and optionally loads a `.env` file.

Example `.env`:

```env
REDIS_URL=redis://127.0.0.1:6380/0
```

Do not commit real secrets or private configuration to Git.

### 5. Start FastAPI

```powershell
uv run uvicorn advanced_api.main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description | Required Scope |
|---|---|---|---|
| GET | `/` | Application status | Public |
| GET | `/health` | Application health response | Public |
| GET | `/items` | Retrieve all items | `read:items` |
| POST | `/items` | Create an item | `write:items` |
| GET | `/items/{item_id}` | Retrieve an item with caching and ETags | `read:items` |
| PUT | `/items/{item_id}` | Update an item with ETag validation | `write:items` |

The application does not expose a public API-key creation endpoint. API keys are managed programmatically through `APIKeyManager`.

## 1. API Key Authentication

API keys authenticate machine clients and determine which operations they can perform.

The application supports two scopes:

- `read:items` — access item retrieval endpoints.
- `write:items` — access item creation and update endpoints.

API keys are generated using Python's `secrets` module. Only their SHA-256 hashes are stored in the API key manager.

Clients provide their key through:

```http
X-API-Key: <your-api-key>
```

### API Key Lifecycle

The `APIKeyManager` supports:

- Key creation
- Key authentication
- Permission validation
- Key revocation
- Key rotation

Missing or invalid keys produce HTTP 401 responses. Insufficient permissions produce HTTP 403 responses.

### Local Development

The API key manager is initialized in memory when the application starts.

For manual API testing, a development key can be generated programmatically through `APIKeyManager`. The application does not automatically provision an API key at startup.

## 2. Idempotent API Requests

Idempotency prevents duplicate operations when clients retry requests because of timeouts, connection failures, or uncertain responses.

**Endpoint:** `POST /items`

Example request:

```http
POST /items
X-API-Key: <write-enabled-api-key>
Idempotency-Key: order-request-001
Content-Type: application/json
```

Request body:

```json
{
  "name": "Mechanical Keyboard",
  "price": 2499.0
}
```

Example successful response:

```json
{
  "item": {
    "id": 1,
    "name": "Mechanical Keyboard",
    "price": 2499.0
  },
  "created_by": "<client-name>"
}
```

When an idempotency key is provided, the API returns:

```text
Idempotency-Replayed: false
```

Reusing the same key with the same request payload returns the previously stored response:

```text
Idempotency-Replayed: true
```

Reusing the key with a different payload produces:

```http
HTTP/1.1 409 Conflict
```

The idempotency manager stores records for **3,600 seconds (1 hour)** and namespaces keys by API client identity.

Idempotency keys are optional for this endpoint. Requests without them execute normally.

## 3. Redis Cache-Aside Pattern

The cache-aside pattern improves repeated data retrieval by checking a cache before loading data from the underlying source.

**Endpoint:** `GET /items/{item_id}`

```text
Client Request
      |
      v
Check Redis Cache
      |
  +---+---+
  |       |
 HIT     MISS
  |       |
  |       v
  |    Load Item
  |       |
  |       v
  |    Store in Redis
  |       |
  +---+---+
      |
      v
Return Response
```

The application uses a **60-second cache TTL**.

Response headers identify cache behavior:

```text
X-Cache: HIT
```

or:

```text
X-Cache: MISS
```

When an item is updated, its cached representation is invalidated.

## 4. HTTP ETags and Conditional Requests

ETags identify versions of resource representations.

The `ETagManager` creates strong ETags by hashing canonical JSON representations using SHA-256.

### Conditional GET

**Endpoint:** `GET /items/{item_id}`

The server includes an ETag in its response:

```http
ETag: "<resource-hash>"
```

A client can send the ETag in a subsequent request:

```http
If-None-Match: "<resource-hash>"
```

If the representation has not changed, the API responds:

```http
HTTP/1.1 304 Not Modified
```

This allows clients to avoid downloading an unchanged response body.

## 5. Optimistic Concurrency Control

Optimistic concurrency control prevents clients from unintentionally overwriting resource changes made by other clients.

**Endpoint:** `PUT /items/{item_id}`

The client must include an `If-Match` header containing the resource's current ETag.

Example:

```http
PUT /items/1
X-API-Key: <write-enabled-api-key>
If-Match: "<current-etag>"
Content-Type: application/json
```

Request body:

```json
{
  "name": "Updated Mechanical Keyboard",
  "price": 2799.0
}
```

Possible responses:

| Status | Meaning |
|---|---|
| 200 | Resource updated |
| 401 | API key missing or invalid |
| 403 | Insufficient permissions |
| 404 | Resource not found |
| 412 | Resource version mismatch |
| 428 | `If-Match` header missing |

On a successful update, the application invalidates the cached representation and returns the new ETag.

## Automated Testing

Run all tests:

```powershell
uv run pytest -v
```

Run tests with coverage:

```powershell
uv run pytest --cov=advanced_api --cov-report=term-missing
```

The seven test modules cover:

- API key authentication
- Cache-aside behavior
- Redis cache integration
- ETag generation and comparison
- Conditional HTTP requests
- Idempotency
- FastAPI integration

## Security and Production Considerations

- Keep raw API keys secret.
- Use HTTPS for authenticated requests.
- Rotate and revoke compromised API keys.
- Apply least-privilege permission scopes.
- Use persistent, shared storage for API keys and idempotency records in production.
- Avoid storing sensitive information in cache entries without appropriate controls.
- Configure Redis authentication and network isolation.
- Review concurrent writes and consistency guarantees.
- Implement monitoring and request tracing.
- Use database transactions for critical operations.

This project demonstrates advanced API design concepts and is not a fully production-deployed service.

## Learning Outcomes

Through Day 17, I explored:

1. Machine-to-machine API authentication.
2. Secure API key generation and hashing.
3. Scope-based authorization.
4. API key rotation and revocation.
5. Idempotent request processing.
6. Redis cache-aside patterns.
7. Cache expiration and invalidation.
8. HTTP ETags and conditional requests.
9. Optimistic concurrency control.
10. Automated testing of advanced API behavior.

---

**Day 17 | 30 Days of Backend Development**

**Author:** YashKhadse01