# Day 21 — Django Authentication Internals

An exploration of Django's authentication and request-processing internals, featuring **custom user models, authentication backends, password hashing, middleware, and automated testing**.

Part of my **30 Days of Backend Development** journey.

## Project Overview

This project demonstrates how Django's built-in authentication framework can be extended to support application-specific requirements.

The implementation includes a custom user model with additional profile fields, an authentication backend that accepts either a username or email address, a custom scrypt-based password hasher, and middleware that measures HTTP request processing time.

The project also demonstrates how these components integrate with Django Admin and Django's testing framework.

## Key Features

- Custom user model extending `AbstractUser`
- Unique email addresses
- Additional phone number field
- User role classification
- Authentication using username or email
- Case-insensitive credential lookup
- Inactive user authentication prevention
- Custom scrypt password hashing
- Salt generation using cryptographically secure randomness
- Constant-time password hash comparison
- Password hash parameter upgrade detection
- Customized Django Admin
- Request-processing middleware
- Response-time measurement
- HTTP request logging
- JSON health-check endpoint
- Automated authentication and middleware tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Programming language |
| Django 5.2 | Web framework |
| SQLite | Development database |
| Django ORM | User data persistence |
| Django Authentication | User authentication framework |
| hashlib.scrypt | Password key derivation |
| Python secrets | Secure salt generation |
| Python logging | Request timing logs |
| Django TestCase | Automated testing |
| pytest | Additional testing tooling |
| pytest-django | Django testing integration |
| Ruff | Code linting |
| uv | Dependency management |

## Project Structure

```text
django_auth_internals/
├── manage.py
├── pyproject.toml
├── README.md
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── backends.py
│   ├── hashers.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── middleware.py
    ├── models.py
    ├── tests.py
    ├── views.py
    └── migrations/
        └── __init__.py
```

## System Architecture

```text
                   HTTP Client
                        |
                        v
                 Django Middleware
                        |
                        v
                  URL Dispatcher
                        |
                        v
                    Django View
                        |
                        v
                  HTTP Response
                        |
                        v
              Request Timing Header
                        |
                        v
                     Client


              Authentication Flow
                        |
                        v
             EmailOrUsernameBackend
                        |
                        v
                 CustomUser Model
                        |
                        v
              CustomScryptPasswordHasher
                        |
                        v
               Credential Verification
```

## Custom User Model

The project defines a `CustomUser` model extending Django's `AbstractUser`.

```python
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
    )

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        DEVELOPER = "developer", "Developer"
        USER = "user", "User"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
```

### Additional User Fields

| Field | Purpose |
|---|---|
| `email` | Unique email address |
| `phone_number` | Optional contact number |
| `role` | User classification |

### Supported Roles

- Admin
- Developer
- User

New users receive the `user` role by default.

These roles are stored as model choices. The current implementation does not include custom role-based authorization rules.

### Django Configuration

```python
AUTH_USER_MODEL = "accounts.CustomUser"
```

This tells Django to use the project's custom user model instead of the default user model.

## Custom Authentication Backend

Django supports pluggable authentication backends.

This project implements:

```python
class EmailOrUsernameBackend(ModelBackend):
    ...
```

The backend extends Django's `ModelBackend` and allows users to authenticate with either their username or email address.

### Authentication Workflow

```text
           Login Credentials
                  |
                  v
        Username or Email Input
                  |
                  v
         Case-Insensitive Lookup
                  |
                  v
            User Record Found?
                  |
             +----+----+
             |         |
            Yes        No
             |         |
             v         v
      Verify Password  Reject
             |
             v
       Check User Active
             |
             v
        Return User / None
```

### Backend Configuration

```python
AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailOrUsernameBackend",
]
```

### Example Usage

Open Django's shell:

```powershell
uv run python manage.py shell
```

Authenticate using a username:

```python
from django.contrib.auth import authenticate

user = authenticate(
    username="testuser",
    password="SecurePassword123!",
)
```

Authenticate using an email:

```python
user = authenticate(
    username="test@example.com",
    password="SecurePassword123!",
)
```

The backend performs case-insensitive matching for usernames and email addresses.

It also rejects invalid passwords and inactive accounts.

## Custom Scrypt Password Hasher

The project implements a custom password hasher extending Django's `BasePasswordHasher`.

```python
class CustomScryptPasswordHasher(BasePasswordHasher):
    algorithm = "custom_scrypt"
```

The implementation uses Python's `hashlib.scrypt` to derive password hashes.

### Configured Parameters

| Parameter | Value |
|---|---|
| Algorithm | scrypt |
| Work factor (`n`) | 16384 |
| Block size (`r`) | 8 |
| Parallelism (`p`) | 1 |
| Derived key length | 64 bytes |
| Salt | 16 random bytes, hex-encoded |

### Password Hashing Process

```text
                Password
                   |
                   v
           Generate Random Salt
                   |
                   v
             hashlib.scrypt
                   |
                   v
            Derived Key Bytes
                   |
                   v
          Encode Hash Parameters
                   |
                   v
          Store Encoded Password
```

### Encoded Hash Format

```text
custom_scrypt$n$r$p$salt$hash
```

The encoded representation stores the algorithm identifier, cost parameters, salt, and derived hash.

### Password Verification

The `verify()` method:

1. Parses the encoded hash.
2. Checks the algorithm identifier.
3. Extracts the hashing parameters.
4. Derives a hash from the supplied password.
5. Compares the result with the stored hash.

The implementation uses Django's `constant_time_compare()`.

### Hash Parameter Updates

The `must_update()` method checks whether stored hashes use the currently configured scrypt parameters.

This supports Django's password-hash upgrade mechanism when hashing parameters change.

### Password Hasher Configuration

```python
PASSWORD_HASHERS = [
    "accounts.hashers.CustomScryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]
```

The custom hasher is the preferred algorithm for newly encoded passwords.

Django can also verify passwords encoded with the other configured algorithms.

## Customized Django Admin

The project extends Django's built-in `UserAdmin` to manage the custom user model.

### Admin Fields

The admin interface includes:

- Username
- Email
- Phone number
- Role
- Staff status
- Active status

### List Filtering

Administrators can filter users by:

- Role
- Staff status
- Active status

### Search

Administrators can search using:

- Username
- Email

The additional user fields are also available in the admin creation and editing forms.

## Custom Request-Timing Middleware

The project implements:

```python
class RequestTimingMiddleware:
    ...
```

The middleware measures the time required to process an HTTP request.

### Middleware Workflow

```text
               Incoming Request
                       |
                       v
              Start Performance Timer
                       |
                       v
                Process Request
                       |
                       v
                Receive Response
                       |
                       v
               Stop Performance Timer
                       |
                       v
                Calculate Duration
                       |
                       v
              Add Response Header
                       |
                       v
                  Log Request
                       |
                       v
                 Return Response
```

### Response Header

The middleware adds:

```http
X-Response-Time-ms: 2.45
```

The numeric value is an illustrative example. Actual response times vary.

### Request Logging

The middleware logs:

- HTTP method
- Request path
- Response status code
- Processing duration in milliseconds

### Middleware Configuration

```python
MIDDLEWARE = [
    # Django middleware...
    "core.middleware.RequestTimingMiddleware",
]
```

The custom middleware runs as part of Django's request-response processing pipeline.

## Health-Check Endpoint

The application exposes a JSON health-check endpoint.

### Request

```http
GET /health/
```

### Response

```json
{
  "status": "success",
  "message": "Day 21 Django Internals API",
  "middleware": "RequestTimingMiddleware"
}
```

The response also includes the `X-Response-Time-ms` header.

## Installation and Setup

### 1. Navigate to the project

From the repository root:

```powershell
cd day21\django_auth_internals
```

### 2. Install Dependencies

Ensure Python 3.11+ and `uv` are installed.

```powershell
uv sync --group dev
```

### 3. Apply Database Migrations

```powershell
uv run python manage.py migrate
```

Django will create the local SQLite database and apply the project's migrations.

### 4. Create a Superuser

```powershell
uv run python manage.py createsuperuser
```

Follow the terminal prompts to create an administrator account.

### 5. Start the Development Server

```powershell
uv run python manage.py runserver
```

Open the health-check endpoint:

```text
http://127.0.0.1:8000/health/
```

Open Django Admin:

```text
http://127.0.0.1:8000/admin/
```

The project uses Django's built-in development server and is not configured for public production deployment.

## Testing

The project uses Django's `TestCase` framework.

Run the complete test suite:

```powershell
uv run python manage.py test
```

Run authentication tests:

```powershell
uv run python manage.py test accounts
```

Run middleware tests:

```powershell
uv run python manage.py test core
```

### Authentication Tests

The test suite covers:

- Custom user model selection
- User creation
- Password hashing
- Correct password verification
- Incorrect password rejection
- Username authentication
- Email authentication
- Incorrect login credentials
- Inactive account authentication rejection

### Middleware Tests

The middleware tests verify:

- Successful health-check responses
- JSON content type
- Presence of the response-time header
- Nonnegative response duration
- Expected health-check response body

## Code Quality

Run Ruff:

```powershell
uv run ruff check .
```

Run Django's configuration checks:

```powershell
uv run python manage.py check
```

Check for unapplied model changes:

```powershell
uv run python manage.py makemigrations --check --dry-run
```

## Security Considerations

The project demonstrates several authentication security concepts:

- Password hashing instead of plaintext storage
- Random salt generation
- Configurable password hashing parameters
- Constant-time hash comparison
- Inactive account rejection
- Django password validation configuration
- Authentication through a custom backend

### Production Hardening Required

Before using this application in production:

1. Replace the hardcoded Django secret key with an environment variable.
2. Disable debug mode.
3. Configure production `ALLOWED_HOSTS`.
4. Enable HTTPS and secure session settings.
5. Review and benchmark password hashing parameters.
6. Add login rate limiting and account abuse protections.
7. Review user permissions separately from role labels.
8. Configure structured logging and monitoring.
9. Protect database credentials and application secrets.
10. Run Django's production deployment checks.

The project is intended for learning and demonstrating Django internals.

## Learning Outcomes

Through Day 21, I explored:

1. Django's authentication architecture.
2. Custom user models with `AbstractUser`.
3. Configuring `AUTH_USER_MODEL`.
4. Implementing custom authentication backends.
5. Username and email authentication.
6. Case-insensitive user lookup.
7. Password hashing with scrypt.
8. Salt generation and hash verification.
9. Password hashing parameter upgrades.
10. Extending Django Admin.
11. Django's middleware lifecycle.
12. Measuring HTTP request duration.
13. Adding custom response headers.
14. Logging HTTP request information.
15. Automated authentication and middleware testing.

---

**Day 21 | 30 Days of Backend Development**

**Author:** YashKhadse01