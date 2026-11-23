# Day 11 — Secure Authentication API

**30-Day Python Backend Development Roadmap | Day 11**

## 1. Project Overview

The Secure Authentication API is a FastAPI-based backend project focused on secure user registration, password protection, email verification, and database-backed security workflows.

The project uses asynchronous PostgreSQL operations, Scrypt password hashing, cryptographically secure verification tokens, and automated security testing.

Its primary objective is to demonstrate how sensitive user credentials and verification processes can be handled safely in a structured backend application.

## 2. Key Features

- Secure user registration
- Email address validation and normalization
- Password strength validation
- Scrypt password hashing with unique random salts
- Constant-time password hash comparison
- Cryptographically secure verification tokens
- SHA-256 token hashing before database storage
- 30-minute verification token expiration
- Single-use email verification tokens
- Atomic database transactions
- Duplicate email protection
- Generic invalid-token error responses
- Development-only email verification logging
- Asynchronous PostgreSQL integration
- Automated API and security testing
- Isolated database test transactions
- Code coverage tooling

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy Async | Asynchronous ORM |
| asyncpg | Async PostgreSQL driver |
| Pydantic | Data validation |
| Pydantic Settings | Environment configuration |
| hashlib.scrypt | Password hashing |
| hashlib.sha256 | Verification token hashing |
| secrets | Secure token and salt generation |
| hmac | Constant-time comparison |
| pytest | Automated testing |
| pytest-asyncio | Async test execution |
| HTTPX | API integration testing |
| Psycopg | Synchronous test database preparation |
| pytest-cov | Coverage reporting |
| uv | Dependency management |

## 4. Project Structure

```text
day11/
├── secure-auth-api/
│   ├── src/
│   │   └── secure_auth_api/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── database.py
│   │       ├── models.py
│   │       ├── schemas.py
│   │       ├── security.py
│   │       ├── tokens.py
│   │       ├── validators.py
│   │       └── email_service.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_registration.py
│   │   ├── test_security.py
│   │   ├── test_email_verification.py
│   │   └── test_email_service.py
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .gitignore
└── README.md
```

## 5. Application Architecture

The project separates API handling, database operations, cryptographic functions, validation, and email delivery into individual modules.

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | API endpoints and registration/verification workflows |
| `database.py` | Async database engine and session management |
| `models.py` | User and verification-token database tables |
| `schemas.py` | Request and response validation |
| `security.py` | Password hashing and verification |
| `tokens.py` | Token generation, hashing, and expiration |
| `validators.py` | Password complexity policy |
| `email_service.py` | Development-only email verification output |

### Registration Flow

```text
Client
  |
  v
POST /auth/register
  |
  v
Validate email and password
  |
  v
Normalize email to lowercase
  |
  v
Check for duplicate user
  |
  v
Hash password using Scrypt
  |
  v
Create user record
  |
  v
Generate secure verification token
  |
  v
Store SHA-256 token hash
  |
  v
Commit database transaction
  |
  v
Attempt verification email delivery
  |
  v
Return safe user response
```

The registration endpoint commits the user and token before attempting email delivery.

If delivery fails, the error is logged and the user remains registered but unverified.

## 6. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check application health |
| POST | `/auth/register` | Register a user |
| POST | `/auth/verify-email` | Verify an email address |

### Health Check

```http
GET /health
```

Expected response:

```json
{
  "status": "healthy"
}
```

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

The response contains the user's ID, email, verification status, and creation timestamp.

Password values and password hashes are excluded from the response.

### Verify Email

```http
POST /auth/verify-email
Content-Type: application/json
```

Example request:

```json
{
  "token": "verification-token-received-during-registration"
}
```

Successful response:

```json
{
  "message": "Email verified successfully"
}
```

An invalid, expired, or previously used token returns HTTP `400`.

## 7. Password Security

Passwords are hashed using Python's `hashlib.scrypt`.

### Hashing Configuration

| Parameter | Value |
|---|---|
| Algorithm | Scrypt |
| N | 16384 |
| r | 8 |
| p | 1 |
| Salt size | 16 bytes |
| Derived key size | 32 bytes |

Each password receives a unique random salt generated with the `secrets` module.

Stored hashes include the algorithm, work parameters, salt, and derived hash.

### Password Verification

The verification function:

1. Parses the stored hash.
2. Validates the algorithm and work parameters.
3. Recomputes the password hash.
4. Compares the derived values using `hmac.compare_digest()`.
5. Returns `False` for malformed or unsupported hashes.

Plaintext passwords are not stored in the database.

## 8. Password Validation Policy

Registration passwords must satisfy the following rules:

| Requirement | Rule |
|---|---|
| Minimum length | 12 characters |
| Maximum length | 128 characters |
| Uppercase | At least one |
| Lowercase | At least one |
| Number | At least one |
| Special character | At least one |

Example valid password:

```text
StrongPass123!
```

Weak or invalid passwords are rejected with HTTP `422`.

## 9. Email Verification Security

Verification tokens are generated using:

```python
secrets.token_urlsafe(32)
```

The raw token is not stored in PostgreSQL.

Instead, its SHA-256 hash is saved in the verification-token table.

### Token Properties

- Cryptographically secure random generation
- SHA-256 hash storage
- 30-minute expiration
- Single-use verification
- Database row locking during verification
- Atomic user verification and token-use updates

### Verification Flow

```text
Client submits token
        |
        v
Hash submitted token
        |
        v
Find matching database record
        |
        v
Lock token row
        |
        v
Check token is unused
        |
        v
Check expiration
        |
        v
Mark user as verified
        |
        v
Mark token as used
        |
        v
Commit transaction
```

Generic error messages are returned for invalid, expired, and previously used tokens.

## 10. Database Design

The application defines two database tables.

### Users Table

| Column | Purpose |
|---|---|
| `id` | Primary key |
| `email` | Unique user email |
| `password_hash` | Scrypt password hash |
| `is_verified` | Email verification status |
| `created_at` | User creation timestamp |

### Email Verification Tokens Table

| Column | Purpose |
|---|---|
| `id` | Primary key |
| `user_id` | Foreign key referencing users |
| `token_hash` | SHA-256 token hash |
| `expires_at` | Token expiration timestamp |
| `used_at` | Timestamp of successful use |
| `created_at` | Token creation timestamp |

The token table uses a foreign key with cascading deletion.

## 11. Installation and Setup

### Prerequisites

- Python 3.11 or newer
- PostgreSQL
- uv
- A configured PostgreSQL database

### Open the Project

From the Day 11 directory:

```powershell
cd secure-auth-api
```

### Install Dependencies

```powershell
uv sync
```

### Configure Environment Variables

Create a local `.env` file:

```dotenv
DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/day11_auth
APP_ENV=development
```

Replace the example database credentials with your own.

Do not commit `.env` files or database passwords.

### Initialize the Database

The reviewed application does not automatically create database tables at startup.

After creating the PostgreSQL database and configuring `DATABASE_URL`, the SQLAlchemy metadata can be used to create missing tables:

```powershell
uv run python -c "import asyncio; from secure_auth_api.database import engine; from secure_auth_api.models import Base; async def setup(): pass"
```

For actual initialization, use a dedicated asynchronous setup script or database migration workflow. The one-line example above is illustrative only and does not create tables.

### Run the API

```powershell
uv run uvicorn secure_auth_api.main:app --reload
```

### Interactive API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

## 12. Development Email Service

The current email service supports local development only.

When:

```dotenv
APP_ENV=development
```

The verification token is written to application logs.

This allows the verification flow to be tested without integrating an external email provider.

When the application environment is not `development`, the email service raises a `RuntimeError`.

The registration endpoint catches this error and logs the delivery failure.

**Security warning:** Development logs containing raw verification tokens must be protected and must not be exposed publicly.

A production email delivery provider is not implemented in the reviewed project.

## 13. Automated Testing

The project uses pytest, pytest-asyncio, and HTTPX.

### Test Modules

| File | Test coverage |
|---|---|
| `test_registration.py` | Registration and duplicate email handling |
| `test_security.py` | Password hashing and validation |
| `test_email_verification.py` | Token verification and reuse prevention |
| `test_email_service.py` | Development and production email behavior |

### Test Case Summary

| Category | Defined cases |
|---|---:|
| Registration | 7 |
| Password security | 17 |
| Email verification | 5 |
| Email service | 2 |
| **Total** | **31** |

The password-security count includes parametrized cases.

## 14. Database Test Isolation

Tests use a dedicated PostgreSQL database:

```text
day11_auth_test
```

The test configuration validates the database name before running database-dependent tests.

### Isolation Strategy

- Dedicated test database
- SQLAlchemy `NullPool`
- Outer database transaction
- Nested savepoints
- Transaction rollback after each test
- FastAPI database dependency overrides
- HTTPX ASGI transport

The test fixture creates missing database tables in the test database.

It does not delete the schema after execution.

### Example Test Configuration

```dotenv
DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/day11_auth
TEST_DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/day11_auth_test
APP_ENV=development
```

Both databases must exist before running the complete test suite.

## 15. Running Tests

Install dependencies:

```powershell
uv sync
```

Run all tests:

```powershell
uv run python -m pytest tests/ -v
```

Run registration tests:

```powershell
uv run python -m pytest tests/test_registration.py -v
```

Run security tests:

```powershell
uv run python -m pytest tests/test_security.py -v
```

Run email verification tests:

```powershell
uv run python -m pytest tests/test_email_verification.py -v
```

The current README documents 31 test cases defined in source code. It does not claim a newly verified passing test run.

## 16. Code Coverage

Generate a terminal coverage report:

```powershell
uv run python -m pytest tests/ --cov=secure_auth_api --cov-report=term-missing
```

Generate an HTML report:

```powershell
uv run python -m pytest tests/ --cov=secure_auth_api --cov-report=html
```

The HTML coverage report is generated in `htmlcov/`.

No coverage percentage is stated without verified execution output.

## 17. Role and Importance of the Project

### User Identity Management

Secure registration provides a foundation for user-based applications.

### Credential Protection

Scrypt hashing reduces the risks associated with storing passwords in plaintext.

### Email Ownership Verification

Email verification helps confirm that users can access their registered email addresses.

### Token Security

Hashed, expiring, single-use tokens reduce the risk of unauthorized token reuse.

### Database Consistency

Atomic commits ensure that related database changes are saved together.

### Security Testing

Automated tests help detect regressions in validation, registration, and verification logic.

### Professional Backend Architecture

Separating database, security, validation, and API logic makes the application easier to maintain and extend.

## 18. Real-World Applications

The techniques demonstrated in this project are relevant to:

- User registration systems
- Customer account platforms
- Employee portals
- SaaS applications
- Enterprise web applications
- Identity verification workflows
- Secure onboarding systems

## 19. Known Limitations

- Login functionality is not implemented in the reviewed API.
- JWT access and refresh tokens are not implemented.
- Authentication-protected endpoints are not included.
- Password reset and account recovery are not implemented.
- Production email delivery is not configured.
- Database migrations are not included in the reviewed source.
- Rate limiting is not implemented.
- Production deployment configuration is not included.

These are potential future enhancements rather than completed Day 11 features.

## 20. Learning Outcomes

Through this project, I practiced:

- Secure API design
- Password hashing with Scrypt
- Random salt generation
- Constant-time password verification
- Secure token generation
- Token hashing and expiration
- Email verification workflows
- SQLAlchemy asynchronous transactions
- Database row locking
- Pydantic validation
- Dependency injection
- Automated security testing
- Database isolation
- Environment-based configuration
- Code coverage analysis

## 21. Day 11 Deliverables

- Secure user registration API
- Email verification endpoint
- Password complexity validation
- Scrypt password hashing
- Hashed verification-token storage
- Single-use verification-token handling
- PostgreSQL user and token models
- Development-only verification email service
- Isolated database testing fixtures
- 31 defined automated test cases
- Code coverage tooling
- Professional project documentation

---

**Roadmap:** 30-Day Python Backend Development  
**Day:** 11  
**Project:** Secure Authentication API  
**Status:** Implementation documented; latest test execution not independently verified