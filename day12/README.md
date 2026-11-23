# Day 12 — Session Authentication API

**30-Day Python Backend Development Roadmap | Day 12**

## 1. Project Overview

The Session Authentication API is a FastAPI-based backend project that implements server-side authentication using PostgreSQL-backed sessions, secure browser cookies, and CSRF protection.

The project builds on earlier authentication concepts by introducing login sessions, authenticated user access, session expiration, session rotation, individual logout, and logout across multiple devices.

Its main objective is to demonstrate how stateful authentication can be implemented and tested in a structured backend application.

## 2. Key Features

- User registration and login
- Scrypt password hashing with random salts
- PostgreSQL-backed authentication sessions
- Cryptographically secure session token generation
- SHA-256 session token hashing
- Configurable session expiration
- HttpOnly authentication cookies
- SameSite=Lax cookie configuration
- Secure cookies in production mode
- Session rotation during reauthentication
- Authenticated user profile endpoint
- Individual session revocation
- Logout from all devices
- Session-bound HMAC-SHA256 CSRF tokens
- CSRF cookie and request-header validation
- Origin and Referer validation
- Automated integration and security tests
- Database transaction isolation

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Programming language |
| FastAPI | REST API development |
| PostgreSQL | Session and user storage |
| SQLAlchemy Async | Asynchronous database access |
| asyncpg | PostgreSQL async driver |
| Pydantic | Request and response validation |
| Pydantic Settings | Environment configuration |
| hashlib.scrypt | Password hashing |
| hashlib.sha256 | Session token hashing |
| hmac | CSRF signatures and secure comparisons |
| secrets | Cryptographically secure token generation |
| pytest | Automated testing |
| pytest-asyncio | Async test execution |
| HTTPX | API integration testing |
| pytest-cov | Code coverage |
| uv | Dependency management |

## 4. Project Structure

```text
day12/
├── session-auth-api/
│   ├── src/
│   │   └── session_auth_api/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── auth.py
│   │       ├── csrf.py
│   │       ├── database.py
│   │       ├── models.py
│   │       ├── schemas.py
│   │       ├── security.py
│   │       └── sessions.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_integration.py
│   │   ├── test_sessions.py
│   │   └── test_session_security.py
│   ├── pyproject.toml
│   └── .gitignore
└── README.md
```

## 5. Application Architecture

The application separates HTTP endpoints, authentication dependencies, cryptographic operations, session handling, and database access.

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | Registration, login, profile, and logout endpoints |
| `auth.py` | Current-user and current-session authentication dependencies |
| `csrf.py` | CSRF token generation, validation, and origin checks |
| `database.py` | Database engine, settings, and session dependency |
| `models.py` | User and session database models |
| `schemas.py` | Request and response schemas |
| `security.py` | Scrypt password hashing and verification |
| `sessions.py` | Session token generation, hashing, and expiration |

### Authentication Flow

```text
Client submits credentials
          |
          v
POST /auth/login
          |
          v
Validate request origin
          |
          v
Validate CSRF if an active session is presented
          |
          v
Verify email and password
          |
          v
Revoke qualifying previous session
          |
          v
Generate a new session token
          |
          v
Store SHA-256 token hash in PostgreSQL
          |
          v
Generate session-bound CSRF token
          |
          v
Set browser cookies
          |
          v
Authenticated session established
```

## 6. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Authenticate and create a session |
| GET | `/auth/me` | Retrieve authenticated user |
| POST | `/auth/logout` | Revoke current session |
| POST | `/auth/logout-all` | Revoke all active sessions |

### Register User

```http
POST /auth/register
Content-Type: application/json
```

Example request:

```json
{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

Successful response: HTTP `201 Created`.

Registration requires a valid email and a password between 12 and 128 characters.

The reviewed Day 12 implementation does not enforce additional password-complexity rules.

### Login

```http
POST /auth/login
Origin: http://127.0.0.1:8000
Content-Type: application/json
```

Example request:

```json
{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

Successful response:

```json
{
  "message": "Login successful"
}
```

The response sets authentication and CSRF cookies.

If an existing active session is presented, its CSRF token must also be supplied in the `X-CSRF-Token` header.

### Current User

```http
GET /auth/me
```

Requires a valid session cookie.

Returns the authenticated user's ID, email, verification status, and creation timestamp.

### Logout

```http
POST /auth/logout
Origin: http://127.0.0.1:8000
X-CSRF-Token: <csrf-token>
```

Requires a valid session, CSRF token, and trusted origin.

Successful response:

```json
{
  "message": "Logged out successfully"
}
```

### Logout from All Devices

```http
POST /auth/logout-all
Origin: http://127.0.0.1:8000
X-CSRF-Token: <csrf-token>
```

Revokes all non-revoked sessions belonging to the authenticated user.

Successful response:

```json
{
  "message": "Logged out from all devices successfully"
}
```

## 7. Password Security

Passwords are hashed using Scrypt with a unique random salt.

| Parameter | Value |
|---|---|
| Algorithm | Scrypt |
| N | 16384 |
| r | 8 |
| p | 1 |
| Salt | 16 bytes |
| Derived key | 32 bytes |

The password verification function checks the stored algorithm, work parameters, salt, and digest before comparing hashes using `hmac.compare_digest()`.

Plaintext passwords are not stored in the database.

## 8. Session Management

Sessions are generated using:

```python
secrets.token_urlsafe(32)
```

Only the SHA-256 hash of each session token is stored in PostgreSQL.

### Session Properties

- Default lifetime: 24 hours
- Configurable expiration
- Unique random token per login
- Database-backed validation
- Revocation timestamp
- Hashed token storage

A session is considered valid when its token hash matches a database record, it has not been revoked, and its expiration time is in the future.

### Session Rotation

When a user logs in again, the application generates a new session token.

If an existing authenticated session belongs to the same user, that presented session is revoked before the new session is issued.

The old token can no longer authenticate once its session has been revoked.

## 9. Cookie Security

The application uses two cookies.

| Property | Session Cookie | CSRF Cookie |
|---|---|---|
| Name | `day12_session` | `day12_csrf` |
| HttpOnly | Yes | No |
| SameSite | Lax | Lax |
| Secure in production | Yes | Yes |
| Path | `/` | `/` |
| Lifetime | Configurable | Matches session lifetime |

The session cookie is HttpOnly to prevent frontend JavaScript from reading the authentication token.

The CSRF cookie is readable by frontend JavaScript so the token can be sent in the `X-CSRF-Token` request header.

## 10. CSRF Protection

The project implements signed, session-bound CSRF tokens.

### Token Generation

A CSRF token contains:

- A random nonce
- An HMAC-SHA256 signature

The signature is calculated using the session token, nonce, and configured secret key.

### Validation Requirements

Protected requests must provide:

1. The authentication session cookie.
2. The CSRF cookie.
3. A matching `X-CSRF-Token` header.
4. A valid HMAC signature for the current session.

Missing, invalid, or modified CSRF tokens result in HTTP `403`.

### Origin Validation

The application accepts these development origins:

```text
http://127.0.0.1:8000
http://localhost:8000
```

For login and logout operations, it checks the `Origin` header or falls back to the `Referer` header.

Requests from untrusted origins are rejected.

These origins are hardcoded for local development and must be adapted before deployment to a different domain.

## 11. Database Design

The application defines two related tables.

### Users Table

| Field | Description |
|---|---|
| `id` | Primary key |
| `email` | Unique user email |
| `password_hash` | Scrypt password hash |
| `is_verified` | Verification status |
| `created_at` | Account creation timestamp |

### Sessions Table

| Field | Description |
|---|---|
| `id` | Primary key |
| `user_id` | Foreign key to users |
| `token_hash` | SHA-256 session token hash |
| `created_at` | Session creation timestamp |
| `expires_at` | Session expiration |
| `revoked_at` | Optional revocation timestamp |

A user can have multiple sessions.

The relationship uses cascading deletion, and an index exists on `user_id` and `expires_at`.

## 12. Installation and Setup

### Prerequisites

- Python 3.11 or newer
- PostgreSQL
- uv
- Separate development and test databases

### Open the Project

From the Day 12 directory:

```powershell
cd session-auth-api
```

### Install Dependencies

```powershell
uv sync
```

### Environment Configuration

Create a local `.env` file:

```dotenv
DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/day12_auth
TEST_DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/day12_auth_test
APP_ENV=development
SESSION_EXPIRE_HOURS=24
SESSION_COOKIE_NAME=day12_session
CSRF_SECRET_KEY=replace-with-a-long-random-secret
```

Generate a secret locally using:

```powershell
uv run python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Use the generated value for `CSRF_SECRET_KEY`.

Never commit real credentials or secret keys to GitHub.

### Database Initialization

The reviewed application does not automatically create database tables at startup.

Create the development and test PostgreSQL databases before running the project.

To create missing tables in the configured development database:

```powershell
@'
import asyncio

from session_auth_api.database import engine
from session_auth_api.models import Base

async def main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()

asyncio.run(main())
'@ | uv run python -
```

This is appropriate for the learning project. Production systems should use versioned database migrations.

### Start the Application

```powershell
uv run uvicorn session_auth_api.main:app --reload
```

### API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

## 13. Automated Testing

The project uses pytest, pytest-asyncio, and HTTPX.

### Test Modules

| File | Purpose |
|---|---|
| `test_integration.py` | End-to-end authentication and session workflows |
| `test_sessions.py` | Session token and expiration behavior |
| `test_session_security.py` | Session uniqueness and CSRF signature security |

### Defined Test Cases

| Category | Cases |
|---|---:|
| Integration | 7 |
| Session utilities | 10 |
| Session security | 3 |
| **Total** | **20** |

### Integration Scenarios

The tests verify:

- Connection to the intended test database
- Health endpoint behavior
- Session rotation after reauthentication
- Revocation across multiple devices
- Rejection of untrusted origins
- Rejection of missing and invalid CSRF tokens
- Rejection of login requests without an accepted origin

### Session Utility Scenarios

The tests verify token generation, uniqueness, hashing, expiration calculations, and rejection of timezone-naive expiration values.

### CSRF Security Scenarios

The tests verify that CSRF tokens are bound to the correct session and that modified signatures are rejected.

## 14. Database Test Isolation

The testing setup uses a separate database configured through `TEST_DATABASE_URL`.

The integration test expects its name to be:

```text
day12_auth_test
```

The shared fixture checks that the development and test database URLs do not point to the same database.

Each test receives:

- A dedicated asynchronous database engine
- An outer transaction
- A SQLAlchemy session using nested savepoints
- A FastAPI database dependency override
- An HTTPX asynchronous client

At the end of each test, the outer transaction is rolled back.

The fixture creates missing tables but does not drop the schema afterward.

## 15. Running Tests

From `session-auth-api`:

```powershell
uv run python -m pytest tests/ -v
```

Run integration tests:

```powershell
uv run python -m pytest tests/test_integration.py -v
```

Run session utility tests:

```powershell
uv run python -m pytest tests/test_sessions.py -v
```

Run security tests:

```powershell
uv run python -m pytest tests/test_session_security.py -v
```

The README documents 20 test cases defined in the source code. The latest passing test count has not been independently verified.

## 16. Code Coverage

Generate a terminal coverage report:

```powershell
uv run python -m pytest tests/ --cov=session_auth_api --cov-report=term-missing
```

Generate an HTML coverage report:

```powershell
uv run python -m pytest tests/ --cov=session_auth_api --cov-report=html
```

The HTML report is generated in `htmlcov/`.

No coverage percentage is claimed without an actual execution report.

## 17. Role and Importance of the Project

### Stateful Authentication

Server-side sessions allow the backend to control whether authentication remains valid.

### Session Revocation

Unlike purely stateless authentication, database-backed sessions can be revoked immediately by updating session records.

### Multi-Device Management

Users can maintain separate sessions on different devices and revoke all sessions when necessary.

### CSRF Protection

Session-bound CSRF tokens help protect cookie-authenticated endpoints against unauthorized cross-site requests.

### Credential Security

Scrypt password hashing protects stored credentials.

### Database Reliability

PostgreSQL stores users and session state, supporting persistent authentication across application restarts.

### Automated Security Testing

Integration and unit tests verify important authentication and security behavior.

## 18. Real-World Applications

The concepts demonstrated in this project apply to:

- Employee portals
- Administrative dashboards
- Enterprise web applications
- Customer account systems
- Internal business platforms
- Browser-based SaaS products
- Applications requiring centralized session revocation

## 19. Known Limitations

- The reviewed API does not implement JWT authentication.
- Email verification is not implemented as an endpoint in this Day 12 project.
- Login does not require `is_verified=True`.
- Registration validates password length but not additional complexity rules.
- Session records are not automatically cleaned up after expiration.
- Database migrations are not included.
- The allowed origins are hardcoded for localhost.
- Rate limiting and account lockout are not implemented.
- Production deployment and monitoring are not included.
- Authentication security depends on protecting database credentials, cookie settings, and the CSRF secret.

## 20. Learning Outcomes

Through Day 12, I practiced:

- Stateful authentication architecture
- Secure session token generation
- SHA-256 token hashing
- PostgreSQL session storage
- Session expiration and revocation
- Authentication dependency injection
- HttpOnly and Secure cookie configuration
- SameSite cookie behavior
- CSRF token signing and verification
- Request origin validation
- Session rotation
- Multi-device logout
- SQLAlchemy relationships
- Asynchronous database testing
- Transaction isolation
- Integration and security testing

## 21. Day 12 Deliverables

- Session-based authentication API
- User registration and login endpoints
- Authenticated profile endpoint
- PostgreSQL-backed session model
- Secure session cookie configuration
- CSRF token generation and validation
- Session rotation on login
- Individual logout
- Logout from all devices
- Database test isolation
- 20 defined automated tests
- Code coverage tooling
- Professional project documentation

---

**Roadmap:** 30-Day Python Backend Development  
**Day:** 12  
**Project:** Session Authentication API  
**Status:** Implementation documented; latest test execution not independently verified