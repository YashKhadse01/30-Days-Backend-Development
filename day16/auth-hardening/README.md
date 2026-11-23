# Day 16 — Authentication Hardening with Redis & FastAPI

A Python backend security project demonstrating **rate limiting, brute-force account lockout, secure password reset tokens, and structured audit logging** using FastAPI and Redis.

Part of my **30 Days of Backend Development** journey.

## Project Overview

Authentication systems require more than password verification. They also need mechanisms to limit abusive requests, defend against repeated login attempts, manage password recovery securely, and record security-relevant events.

This project implements four security components backed by Redis, with dedicated demonstration endpoints and automated tests.

## Key Features

- Redis-backed sliding-window rate limiting
- Atomic rate-limit operations using Redis Lua scripts
- Account lockout after repeated failed login attempts
- Configurable lockout thresholds and durations
- Cryptographically generated password reset tokens
- SHA-256 hashing of reset tokens before Redis storage
- Single-use password reset token consumption
- Structured audit event logging
- API-key protection for password reset demonstration endpoints
- FastAPI health checks and integration tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend programming |
| FastAPI | REST API framework |
| Redis | Shared security state and token storage |
| redis-py (asyncio) | Asynchronous Redis operations |
| Redis Lua | Atomic security operations |
| Argon2-cffi | Password hashing dependency |
| Pydantic Settings | Configuration dependency |
| Uvicorn | ASGI application server |
| pytest | Automated testing |
| pytest-asyncio | Asynchronous testing |
| fakeredis | Redis test doubles |
| HTTPX | API integration testing |
| pytest-cov | Test coverage |
| uv | Dependency management |

## Project Structure

```text
auth-hardening/
├── pyproject.toml
├── README.md
├── src/
│   └── auth_hardening/
│       ├── __init__.py
│       ├── main.py
│       ├── rate_limiter.py
│       ├── lockout.py
│       ├── password_reset.py
│       └── audit_log.py
└── tests/
    ├── test_api_integration.py
    ├── test_audit_log.py
    ├── test_lockout.py
    ├── test_password_reset.py
    └── test_rate_limiter.py
```

## Architecture

```text
Client
   |
   v
FastAPI Application
   |
   +-- Rate Limiting
   |      |
   |      +-- Redis Sliding Window
   |
   +-- Failed Login Simulation
   |      |
   |      +-- Redis Account Lockout
   |
   +-- Password Reset Demo
   |      |
   |      +-- Token Generation
   |      +-- Token Hashing
   |      +-- Single-Use Consumption
   |
   +-- Security Audit Logger
          |
          +-- Redis Audit Records
```

Redis provides shared storage for request counters, lockout state, reset-token records, and security events.

## Installation and Setup

### 1. Navigate to the project

From the repository root:

```powershell
cd day16\auth-hardening
```

### 2. Install dependencies

Ensure Python 3.11+ and `uv` are installed.

```powershell
uv sync --group dev
```

### 3. Start Redis

The application requires a running Redis server.

If Docker Desktop is available:

```powershell
docker run -d --name day16-redis -p 6379:6379 redis:7-alpine
```

If a container with that name already exists but is stopped:

```powershell
docker start day16-redis
```

Check connectivity:

```powershell
docker exec day16-redis redis-cli ping
```

Expected response:

```text
PONG
```

### 4. Configure Redis

The application reads the `REDIS_URL` environment variable.

Its default value is:

```text
redis://127.0.0.1:6379/0
```

To set it explicitly in PowerShell:

```powershell
$env:REDIS_URL = "redis://127.0.0.1:6379/0"
```

### 5. Start FastAPI

```powershell
uv run uvicorn auth_hardening.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application status |
| GET | `/health` | Redis-backed health check |
| GET | `/demo/rate-limit` | Demonstrate sliding-window rate limiting |
| POST | `/demo/login-failure` | Simulate failed login attempts and account lockout |
| POST | `/demo/password-reset/create` | Generate a single-use reset token |
| POST | `/demo/password-reset/consume` | Validate and consume a reset token |

The password reset demonstration endpoints require an `X-Demo-Key` header.

## 1. Sliding-Window Rate Limiting

**Endpoint:** `GET /demo/rate-limit`

The endpoint permits up to five requests per client identity within a 60-second sliding window.

When the limit is exceeded, the API returns:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

Example response:

```json
{
  "detail": "Too many requests"
}
```

### Implementation

The `SlidingWindowRateLimiter` uses Redis sorted sets and a Lua script to:

1. Remove timestamps outside the active window.
2. Count requests remaining within the window.
3. Reject requests exceeding the configured limit.
4. Record permitted requests.
5. Set a Redis key expiration.

The Lua script performs these operations atomically.

## 2. Brute-Force Account Lockout

**Endpoint:** `POST /demo/login-failure`

Example request:

```json
{
  "account": "example_user"
}
```

The endpoint simulates failed authentication attempts.

Default lockout settings:

| Setting | Value |
|---|---|
| Maximum failed attempts | 5 |
| Attempt window | 300 seconds |
| Account lockout duration | 300 seconds |

Account identifiers are normalized using whitespace trimming and case folding.

After the lockout threshold is reached, the API returns HTTP 429 with a `Retry-After` header.

The `BruteForceProtector` module also provides a `record_success()` method for clearing recorded failures after successful authentication.

**Important:** This endpoint simulates failed logins; it does not implement a complete username/password login system.

## 3. Secure Password Reset Tokens

The `PasswordResetManager` implements token generation, storage, expiration, and one-time consumption.

### Token Generation

Reset tokens are generated using Python's `secrets` module.

The raw token is returned to the caller, while its SHA-256 digest is used to construct the Redis storage key.

Default token validity:

```text
900 seconds (15 minutes)
```

### Create a Reset Token

**Endpoint:** `POST /demo/password-reset/create`

First configure a local demonstration API key:

```powershell
$env:DAY16_DEMO_KEY = "replace-with-a-long-random-local-secret"
```

Set this variable before starting the FastAPI server.

Example request body:

```json
{
  "user_id": "user123"
}
```

Required header:

```text
X-Demo-Key: <your-demo-key>
```

Successful response structure:

```json
{
  "reset_token": "<generated-reset-token>"
}
```

### Consume a Reset Token

**Endpoint:** `POST /demo/password-reset/consume`

Example request:

```json
{
  "token": "<generated-reset-token>"
}
```

Successful response structure:

```json
{
  "message": "Reset token consumed",
  "user_id": "user123"
}
```

Token consumption uses a Redis Lua script that atomically retrieves and deletes the token record.

An expired, invalid, or previously consumed token is rejected.

**Important:** These endpoints demonstrate reset-token lifecycle management only. They do not update account passwords or send password reset emails. Returning raw reset tokens is intended strictly for protected local demonstrations.

## 4. Security Audit Logging

The `AuditLogger` module records structured security events in Redis.

Supported event types include:

| Event | Description |
|---|---|
| `login_success` | Successful authentication event |
| `login_failure` | Failed authentication event |
| `account_locked` | Account lockout event |
| `rate_limited` | Request rejected by rate limiter |
| `password_reset_requested` | Password reset token requested |
| `password_reset_completed` | Password reset completion event type |
| `logout` | Logout event type |

These are supported event types; not every event is emitted by the demonstration API.

Each audit record contains:

```json
{
  "event": "login_failure",
  "user_id": null,
  "ip_address": null,
  "timestamp": 0
}
```

The timestamp above is illustrative.

The logger stores approved fields only and provides a method to retrieve recent audit records.

## Automated Testing

Run the full test suite:

```powershell
uv run pytest -v
```

Run tests with coverage:

```powershell
uv run pytest --cov=auth_hardening --cov-report=term-missing
```

Test modules cover:

- Rate limiting
- Account lockout
- Password reset tokens
- Audit logging
- FastAPI integration

The project includes `fakeredis` for testing Redis-dependent functionality.

## Security Considerations

- Never expose password reset tokens through public production endpoints.
- Store API keys and credentials outside version control.
- Keep Redis protected from unauthorized network access.
- Use HTTPS for production authentication services.
- Disable `DAY16_TESTING` in production.
- Do not expose demonstration endpoints without appropriate controls.
- Use reliable client identification behind trusted reverse proxies.
- Apply least-privilege access to Redis.
- Protect audit records from unauthorized modification.
- Establish audit log retention and monitoring policies.
- Review lockout behavior to reduce denial-of-service risks.

This project is an educational security demonstration and requires additional hardening before production deployment.

## Learning Outcomes

Through Day 16, I explored:

1. Sliding-window rate limiting.
2. Redis sorted sets and atomic Lua scripts.
3. Brute-force protection and account lockout.
4. Secure random token generation.
5. Hashed password reset token storage.
6. Token expiration and single-use consumption.
7. Structured authentication audit logging.
8. FastAPI security dependencies.
9. Redis-backed asynchronous application design.
10. Automated security testing.

---

**Day 16 | 30 Days of Backend Development**

**Author:** YashKhadse01