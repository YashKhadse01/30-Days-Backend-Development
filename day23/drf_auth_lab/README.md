# Day 23 — Django REST Framework Authentication Lab

A security-focused authentication project built using **Django REST Framework (DRF)**, implementing custom JWT authentication, access and refresh tokens, refresh-token rotation, token-family revocation, TOTP-based two-factor authentication, and replay protection.

Part of my **30 Days of Backend Development** journey.

## Project Overview

This project explores the internal workings of modern API authentication and token lifecycle management.

Instead of relying on a complete third-party JWT authentication package, the project implements custom authentication components using PyJWT, PyOTP, Django ORM, and Django REST Framework.

The application demonstrates how to authenticate users, issue short-lived access tokens, maintain server-side refresh-token records, detect refresh-token reuse, and require time-based one-time passwords for users with verified TOTP devices.

The project is intended for educational use and requires additional security hardening before production deployment.

## Key Features

- Custom JWT authentication backend
- Bearer token authentication
- JWT creation and verification with PyJWT
- HS256 token signing
- 15-minute access-token lifetime
- JWT issuer and audience validation
- Required JWT claims and token-type validation
- Protected user profile endpoint
- Seven-day opaque refresh tokens
- Cryptographically random refresh-token generation
- SHA-256 hashing of stored refresh tokens
- Refresh-token rotation
- Refresh-token family tracking
- Refresh-token reuse detection
- Token-family revocation
- Inactive-user authentication rejection
- TOTP-based two-factor authentication
- TOTP secret generation and provisioning URI support
- TOTP replay protection
- Database transactions for token operations
- Automated authentication and security tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Programming language |
| Django 5.2 | Web framework |
| Django REST Framework | API development and authentication integration |
| PyJWT | JWT signing and verification |
| PyOTP | Time-based one-time password generation and verification |
| SQLite | Development database |
| Django ORM | Token and device persistence |
| Python secrets | Secure random token generation |
| hashlib | Refresh-token hashing |
| pytest | Testing tooling |
| pytest-django | Django testing integration |
| Ruff | Code linting |
| uv | Dependency management |

## Project Structure

```text
drf_auth_lab/
├── manage.py
├── pyproject.toml
├── README.md
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── authentication/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── backends.py
│   ├── jwt_utils.py
│   ├── login_views.py
│   ├── models.py
│   ├── refresh_utils.py
│   ├── refresh_views.py
│   ├── totp_utils.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   ├── test_jwt.py
│   ├── test_login.py
│   ├── test_refresh_api.py
│   ├── test_totp.py
│   ├── test_totp_replay.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
└── config/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Application Architecture

```text
                       API Client
                           |
                           v
                     Django URLs
                           |
              +------------+------------+
              |            |            |
              v            v            v
           Login         Refresh      Profile
              |            |            |
              v            v            v
        Django Auth    Refresh Token   JWT Auth
              |         Rotation       Backend
              v            |            |
         TOTP Check        v            v
              |       Token Database  JWT Verify
              v            |            |
        Issue Tokens       v            v
              |       Issue New Pair  User Lookup
              |                         |
              +------------+------------+
                           |
                           v
                       Response
```

### Module Responsibilities

**accounts**

Contains the `TOTPDevice` model for associating a TOTP secret and replay-protection state with a Django user.

**authentication**

Implements JWT handling, login, refresh-token rotation, TOTP verification, authentication middleware integration through DRF, and the protected profile endpoint.

**config**

Contains Django settings, root URL routing, and application configuration.

## Authentication Endpoints

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| POST | `/api/login/` | Not required | Authenticate credentials and issue tokens |
| POST | `/api/refresh/` | Refresh token in body | Rotate refresh token and issue new tokens |
| GET | `/api/profile/` | Valid Bearer access token | Retrieve authenticated user details |

The Django administration route is also configured at `/admin/`.

The project does not implement public registration, logout, password reset, or TOTP enrollment API endpoints.

## JWT Access Tokens

The project uses PyJWT to create signed access tokens.

### Configuration

```python
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 15
ISSUER = "day23-drf-auth"
AUDIENCE = "day23-api"
```

### JWT Claims

| Claim | Purpose |
|---|---|
| `sub` | User identifier |
| `type` | Token type (`access`) |
| `jti` | Unique token identifier |
| `iat` | Issued-at timestamp |
| `nbf` | Not-before timestamp |
| `exp` | Expiration timestamp |
| `iss` | Token issuer |
| `aud` | Intended audience |

The JWT is signed using Django's `SECRET_KEY`.

### Access Token Creation

```python
def create_access_token(user):
    now = datetime.now(UTC)

    payload = {
        "sub": str(user.pk),
        "type": "access",
        "jti": str(uuid.uuid4()),
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=15),
        "iss": ISSUER,
        "aud": AUDIENCE,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256",
    )
```

### JWT Verification

The implementation validates:

- Token signature
- Allowed signing algorithm
- Issuer
- Audience
- Required claims
- Expiration
- Token type
- Subject data type

A valid token must also reference an existing, active Django user.

## Custom JWT Authentication Backend

The application implements:

```python
class JWTAuthentication(BaseAuthentication):
    ...
```

The backend reads the HTTP `Authorization` header and expects a Bearer token.

### Authentication Flow

```text
                 HTTP Request
                      |
                      v
              Authorization Header
                      |
                      v
                Bearer Token?
                      |
                      v
                Decode JWT
                      |
                      v
           Validate Claims and Signature
                      |
                      v
              Retrieve Django User
                      |
                      v
               Is User Active?
                      |
                +-----+-----+
                |           |
               Yes          No
                |           |
                v           v
         Authenticate      Reject
```

### DRF Configuration

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "authentication.backends.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

All DRF endpoints require authentication by default unless they explicitly override the permission policy.

The login and refresh endpoints use `AllowAny` and disable authentication classes.

## Login Workflow

**POST** `/api/login/`

### Request Without TOTP

```json
{
  "username": "demo_user",
  "password": "ExamplePassword123!"
}
```

### Request With TOTP

```json
{
  "username": "demo_user",
  "password": "ExamplePassword123!",
  "totp_code": "123456"
}
```

The TOTP code above is illustrative.

### Login Processing

1. Validate username and password input types.
2. Authenticate credentials using Django's authentication system.
3. Check whether the user has a verified TOTP device.
4. Require a valid, unused TOTP code when a verified device exists.
5. Generate a signed access token.
6. Generate and store a hashed refresh token.
7. Return the access and refresh tokens.

### Successful Response

```json
{
  "access": "<signed-jwt-access-token>",
  "refresh": "<opaque-refresh-token>",
  "token_type": "Bearer"
}
```

### Login Failure Cases

| Condition | HTTP Status |
|---|---|
| Invalid credential input types | 400 |
| Incorrect username or password | 401 |
| Missing TOTP for a verified device | 401 |
| Invalid or replayed TOTP | 401 |

A user without a verified TOTP device can authenticate using username and password alone.

## Refresh Token Management

The project uses opaque refresh tokens rather than JWT refresh tokens.

Refresh tokens are generated using:

```python
secrets.token_urlsafe(48)
```

Only their SHA-256 hashes are stored in the database.

### Refresh Token Lifetime

```python
REFRESH_TOKEN_DAYS = 7
```

Each generated refresh token expires seven days after creation.

### RefreshToken Model

| Field | Purpose |
|---|---|
| `id` | UUID primary key |
| `user` | Associated Django user |
| `token_hash` | Unique SHA-256 hash |
| `family_id` | Refresh-token family identifier |
| `expires_at` | Expiration timestamp |
| `revoked_at` | Revocation timestamp |
| `replaced_by` | Replacement token record |
| `created_at` | Creation timestamp |

### Refresh Token Hashing

```python
def hash_refresh_token(token):
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()
```

The raw refresh token is returned to the client but is not stored directly in the `RefreshToken` model.

## Refresh Token Rotation

**POST** `/api/refresh/`

### Request

```json
{
  "refresh": "<current-refresh-token>"
}
```

### Successful Response

```json
{
  "access": "<new-access-token>",
  "refresh": "<new-refresh-token>",
  "token_type": "Bearer"
}
```

### Rotation Process

```text
              Current Refresh Token
                        |
                        v
                  Hash Token
                        |
                        v
               Find Token Record
                        |
                        v
                Validate Record
                        |
                        v
               Create Replacement
                        |
                        v
               Revoke Old Token
                        |
                        v
                 Link Replacement
                        |
                        v
              Return New Token Pair
```

The rotation logic runs inside a database transaction and uses `select_for_update()` to request a row-level lock where supported by the database.

The implementation creates a new refresh token for each successful refresh operation. The new token retains the same family identifier.

## Refresh Token Reuse Detection

The application tracks refresh tokens by family.

When a previously revoked refresh token is presented again, the rotation logic treats the event as reuse.

### Reuse Detection Flow

```text
                Refresh Request
                       |
                       v
                Find Token Record
                       |
                       v
               Already Revoked?
                       |
                +------+------+
                |             |
               Yes            No
                |             |
                v             v
         Revoke Active      Continue
         Family Tokens      Validation
                |
                v
             Reject
```

The implementation revokes unrevoked tokens belonging to the detected token family.

This reduces the usefulness of replacement refresh tokens after reuse of an older token is detected.

### Important Limitation

Refresh-token family revocation does not automatically invalidate previously issued JWT access tokens.

Those tokens remain independently verifiable until expiration unless additional access-token revocation controls are implemented.

## TOTP-Based Two-Factor Authentication

The project uses PyOTP for time-based one-time password verification.

TOTP provides an additional authentication factor for users who have a verified TOTP device.

### TOTPDevice Model

| Field | Purpose |
|---|---|
| `user` | One-to-one Django user relationship |
| `secret` | TOTP shared secret |
| `is_verified` | Whether the device is verified |
| `last_used_step` | Last accepted TOTP time step |
| `created_at` | Creation timestamp |

### TOTP Secret Generation

```python
def generate_totp_secret():
    return pyotp.random_base32()
```

### Provisioning URI

```python
def generate_totp_uri(secret, username):
    return pyotp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name="Day23AuthLab",
    )
```

The provisioning URI can be used with compatible authenticator applications.

The current project provides utility functions but does not expose a public enrollment endpoint or QR-code generation API.

### TOTP Verification

The implementation uses:

```python
pyotp.TOTP(secret).verify(
    str(code),
    valid_window=0,
)
```

A zero verification window means adjacent time steps are not accepted.

## TOTP Replay Protection

A standard TOTP code may remain valid during its time window.

The project adds replay protection by recording the last accepted time step.

### Replay Protection Workflow

```text
                   TOTP Code
                       |
                       v
              Find Verified Device
                       |
                       v
               Current Time Step
                       |
                       v
             Compare Last Used Step
                       |
                       v
             Already Used This Step?
                       |
                +------+------+
                |             |
               Yes            No
                |             |
                v             v
              Reject      Verify Code
                               |
                               v
                          Save Time Step
                               |
                               v
                             Accept
```

The function `verify_totp_once()` uses a database transaction and `select_for_update()` to coordinate verification and state updates.

This helps prevent repeated acceptance of the same TOTP time step.

Database-specific locking behavior must be considered when deploying with multiple concurrent requests.

## Protected Profile Endpoint

**GET** `/api/profile/`

### Request

```http
GET /api/profile/
Authorization: Bearer <access-token>
```

### Example Response

```json
{
  "message": "JWT authentication successful",
  "user_id": 1,
  "username": "demo_user"
}
```

The user ID and username are illustrative.

The endpoint requires a valid access token belonging to an active user.

Missing, invalid, expired, or otherwise unacceptable access tokens result in authentication failure.

## Installation and Setup

### 1. Navigate to the Project

From the repository root:

```powershell
cd day23\drf_auth_lab
```

### 2. Install Dependencies

Python 3.11+ and `uv` are required.

```powershell
uv sync --group dev
```

### 3. Configure the Django Secret Key

The supplied development code contains a hardcoded secret key.

For safer local configuration, update `config/settings.py` to read the key from the environment before running the following commands.

Generate a new secret in PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
$env:DJANGO_DEBUG = "True"
```

The environment variable names above assume the corresponding changes have been made to `settings.py`.

### 4. Apply Migrations

```powershell
uv run python manage.py migrate
```

### 5. Create a Test User

```powershell
uv run python manage.py createsuperuser
```

This creates a Django user that can be used for local authentication testing.

### 6. Start the Development Server

```powershell
uv run python manage.py runserver
```

The application will be accessible locally at:

```text
http://127.0.0.1:8000/
```

### 7. Test Authentication

Send a POST request to:

```text
http://127.0.0.1:8000/api/login/
```

Supply the username and password of the test user.

If no verified TOTP device is configured, the login response should include access and refresh tokens.

Use the returned access token in the `Authorization` header when requesting `/api/profile/`.

## Automated Testing

The project includes 24 explicit test methods across five test modules.

### JWT Authentication Tests

`authentication/test_jwt.py`

Covers:

- Valid JWT authentication
- Missing access token
- Invalid access token
- Disabled user rejection

### Login Integration Tests

`authentication/test_login.py`

Covers:

- Login without TOTP
- Incorrect password
- Missing TOTP code
- Valid TOTP code
- Replayed TOTP code

### Refresh API Tests

`authentication/test_refresh_api.py`

Covers:

- Successful refresh-token rotation
- Missing refresh token
- Invalid refresh token
- Refresh-token reuse and family revocation
- Disabled user refresh rejection

### TOTP Utility Tests

`authentication/test_totp.py`

Covers:

- TOTP secret generation
- Provisioning URI generation
- Valid TOTP verification
- Invalid TOTP rejection
- Missing TOTP rejection

### TOTP Replay Tests

`authentication/test_totp_replay.py`

Covers:

- Valid one-time code acceptance
- Replayed code rejection
- Invalid code rejection
- Unverified device rejection
- Missing device rejection

### Run the Complete Test Suite

```powershell
uv run python manage.py test
```

### Run Authentication Tests

```powershell
uv run python manage.py test authentication
```

### Run Django System Checks

```powershell
uv run python manage.py check
```

### Check for Model Changes

```powershell
uv run python manage.py makemigrations --check --dry-run
```

### Run Ruff

```powershell
uv run ruff check .
```

Test coverage is described from the supplied source code; passing results must be confirmed by executing the tests.

## Security Considerations

The project demonstrates several important authentication protections:

- Signed JWT access tokens
- Short access-token lifetime
- Required JWT claims
- Issuer and audience validation
- Active-user checks
- Cryptographically random refresh tokens
- Hashed refresh-token storage
- Refresh-token rotation
- Token-family reuse detection
- TOTP-based additional authentication
- TOTP replay prevention
- Database transactions for state changes

### Production Hardening Requirements

Before production use, the application should address:

1. Environment-based secret-key configuration and secret rotation.
2. Disabling Django debug mode.
3. HTTPS and secure deployment settings.
4. Login rate limiting and brute-force protection.
5. Refresh endpoint rate limiting.
6. Secure TOTP secret storage and enrollment procedures.
7. TOTP recovery and device revocation workflows.
8. Token revocation and logout requirements.
9. Multi-worker concurrency and database-locking behavior.
10. Security logging, monitoring, and automated deployment checks.

The project is a learning implementation rather than a production-ready identity provider.

## Learning Outcomes

Through Day 23, I explored:

1. Django REST Framework authentication architecture.
2. Custom Bearer authentication backends.
3. JWT creation and signature verification.
4. JWT claims and expiration handling.
5. Issuer and audience validation.
6. Access-token authentication.
7. Opaque refresh-token generation.
8. Secure refresh-token storage using hashes.
9. Refresh-token rotation.
10. Refresh-token family tracking.
11. Refresh-token reuse detection.
12. Transactional token management.
13. TOTP-based two-factor authentication.
14. TOTP provisioning URI generation.
15. TOTP replay protection.
16. Protected REST API endpoints.
17. Automated authentication and security testing.
18. Production security considerations.

---

**Day 23 | 30 Days of Backend Development**

**Author:** YashKhadse01