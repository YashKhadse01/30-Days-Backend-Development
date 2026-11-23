# Day 14 — Two-Factor Authentication (2FA) & Role-Based Access Control (RBAC)

A Python backend security project implementing multi-factor authentication and permission-based authorization using **FastAPI**, **Argon2id**, and **Time-Based One-Time Passwords (TOTP)**.

Part of my **30 Days of Backend Development** journey.

## Project Overview

This project explores how secure backend authentication systems combine password verification, a second authentication factor, session management, and role-based permissions.

The application requires users to complete two authentication stages before accessing protected resources.

**Authentication flow:**

```text
User
  |
  v
POST /auth/login
  |
  v
Password Verification
  |
  v
Temporary Challenge Token
  |
  v
POST /auth/verify-2fa
  |
  v
TOTP Verification
  |
  v
Bearer Session Token
  |
  v
Protected API Endpoints
  |
  v
RBAC Permission Check
```

## Features

- Password authentication using Argon2id
- TOTP-based two-factor authentication
- Temporary authentication challenges
- Bearer-token session authentication
- Authenticated user profile endpoint
- Session logout and revocation
- Role-based access control
- Permission-protected API endpoints
- Backup-code functionality organized in a dedicated module
- Authenticator integration utilities
- Automated authentication and security tests
- Optional development demo account

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend programming language |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| Argon2-cffi | Password hashing |
| Cryptography | Cryptographic operations |
| QRCode | QR code generation |
| Pillow | Image processing |
| HTTPX | HTTP client and API testing |
| pytest | Automated testing |
| pytest-cov | Test coverage |
| uv | Dependency and environment management |

## Project Structure

```text
auth-2fa-rbac/
├── .gitignore
├── pyproject.toml
├── README.md
├── verify_authenticator.py
├── day14_authenticator_test.png
├── src/
│   └── auth_2fa_rbac/
│       ├── __init__.py
│       ├── main.py
│       ├── authenticator.py
│       ├── auth_service.py
│       ├── backup_codes.py
│       ├── rbac.py
│       ├── security.py
│       └── totp.py
└── tests/
    ├── test_api_integration.py
    ├── test_auth_edge_cases.py
    ├── test_auth_flow.py
    ├── test_backup_codes.py
    ├── test_rbac.py
    ├── test_security.py
    └── test_totp.py
```

The development-only `.totp_test_secret` file may be generated locally when demo mode is enabled. It should not be committed to version control.

## Installation and Setup

### 1. Navigate to the project

From the repository root:

```powershell
cd day14\auth-2fa-rbac
```

### 2. Install dependencies

Ensure Python 3.11+ and `uv` are installed.

```powershell
uv sync --group dev
```

### 3. Start the FastAPI server

```powershell
uv run uvicorn auth_2fa_rbac.main:app --reload
```

The application runs locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Enable the development demo account (optional)

In PowerShell, before starting the server:

```powershell
$env:DAY14_DEMO_MODE = "1"
uv run uvicorn auth_2fa_rbac.main:app --reload
```

The application initializes the following development account:

```text
Username: testuser
Password: StrongPassword123!
Role: user
```

The associated TOTP secret is read from or written to `.totp_test_secret`.

**Security warning:** Demo mode is for local testing only. Never enable it in production or expose the demo credentials publicly on a deployed application.

To disable demo mode in the current PowerShell session:

```powershell
Remove-Item Env:DAY14_DEMO_MODE
```

## API Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/` | Application information | Public |
| GET | `/health` | Health check | Public |
| POST | `/auth/login` | Verify username and password | Public |
| POST | `/auth/verify-2fa` | Complete two-factor authentication | Challenge token + OTP |
| GET | `/auth/me` | Retrieve authenticated user profile | Bearer token |
| POST | `/auth/logout` | Revoke the current session | Bearer token |
| GET | `/reports` | Retrieve reports | `REPORTS_READ` permission |
| POST | `/reports` | Create a report | `REPORTS_CREATE` permission |
| GET | `/admin/users` | Access user management endpoint | `USERS_MANAGE` permission |

## Authentication Workflow

### Step 1 — Password Verification

**Endpoint:** `POST /auth/login`

Request:

```json
{
  "username": "testuser",
  "password": "StrongPassword123!"
}
```

Successful response structure:

```json
{
  "message": "Password verified. 2FA required.",
  "challenge_token": "<temporary-challenge-token>",
  "expires_in": 300
}
```

The response indicates a challenge lifetime of 300 seconds.

### Step 2 — Two-Factor Verification

**Endpoint:** `POST /auth/verify-2fa`

Request:

```json
{
  "challenge_token": "<temporary-challenge-token>",
  "otp": "<current-six-digit-code>"
}
```

Successful response structure:

```json
{
  "message": "Two-factor authentication successful",
  "session_token": "<session-token>",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

The response indicates a session lifetime of 1,800 seconds.

### Step 3 — Access Protected Resources

Send the session token in the Authorization header:

```text
Authorization: Bearer <session-token>
```

For example:

```http
GET /auth/me
Authorization: Bearer <session-token>
```

The endpoint returns the authenticated username, role, and two-factor authentication status.

### Step 4 — Logout

**Endpoint:** `POST /auth/logout`

The application calls the session revocation service to invalidate the current session token.

## Role-Based Access Control

RBAC restricts access to resources based on the authenticated user's assigned role and permissions.

The application checks the following permissions:

| Permission | Protected Operation |
|---|---|
| `REPORTS_READ` | GET `/reports` |
| `REPORTS_CREATE` | POST `/reports` |
| `USERS_MANAGE` | GET `/admin/users` |

The role-to-permission mappings are defined in `rbac.py`.

Authentication and authorization errors are handled separately:

- **401 Unauthorized:** Missing, invalid, or expired authentication.
- **403 Forbidden:** Authenticated user lacks the required permission.

## Two-Factor Authentication

TOTP generates time-dependent verification codes using a shared secret.

The project includes dedicated modules for TOTP operations and authenticator integration.

Backup-code functionality is implemented separately in `backup_codes.py`, with corresponding automated tests.

## Automated Testing

Run the complete test suite:

```powershell
uv run pytest -v
```

Run tests with coverage:

```powershell
uv run pytest --cov=auth_2fa_rbac --cov-report=term-missing
```

The test suite is organized into seven modules:

- `test_api_integration.py` — API integration
- `test_auth_edge_cases.py` — Authentication edge cases
- `test_auth_flow.py` — Authentication workflow
- `test_backup_codes.py` — Backup-code functionality
- `test_rbac.py` — Role-based authorization
- `test_security.py` — Security operations
- `test_totp.py` — Time-based one-time passwords

## Security Considerations

- Never store plaintext passwords.
- Protect TOTP secrets and authentication tokens.
- Never commit `.totp_test_secret` or other credentials.
- Use HTTPS when deploying authentication services.
- Disable demo mode in production.
- Apply appropriate rate limiting to login and OTP verification.
- Store authentication state securely in production systems.
- Apply least-privilege authorization rules.
- Review session expiration and revocation behavior before production use.

This project is intended for educational and local development purposes. Additional security review and infrastructure hardening would be required before production deployment.

## Learning Outcomes

Through Day 14, I explored:

1. Password-based authentication with Argon2id.
2. Multi-factor authentication using TOTP.
3. Two-stage authentication workflows.
4. Temporary challenges and authenticated sessions.
5. Bearer-token authentication in FastAPI.
6. Role-based access control and permission checks.
7. Session revocation and logout.
8. Backup-code and authenticator integration concepts.
9. Automated testing of security-sensitive backend functionality.

---

**Day 14 | 30 Days of Backend Development**

**Author:** YashKhadse01