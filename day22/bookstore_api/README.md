# Day 22 — Bookstore REST API

A versioned RESTful Bookstore API developed using **Django REST Framework (DRF)**, demonstrating CRUD operations, nested serializers, advanced filtering, API permissions, request throttling, OpenAPI documentation, and automated API testing.

Part of my **30 Days of Backend Development** journey.

## Project Overview

This project demonstrates the design and implementation of a structured REST API for managing authors, books, and their associated reviews.

The application uses Django REST Framework to expose versioned endpoints, enforce access restrictions, validate nested data, and support flexible querying.

The project also explores practical API engineering concepts, including rate limiting, OpenAPI schema generation, and automated endpoint verification.

## Key Features

- RESTful CRUD operations for authors and books
- API versioning using URL paths
- Django REST Framework `ModelViewSet`
- Model-based serializers
- Nested review serialization
- Atomic nested create and update operations
- Book filtering by author
- Book search by title, description, and author name
- Book ordering by price, creation date, and title
- Custom staff-only book modification permissions
- Read-only access for unauthenticated users
- Anonymous and authenticated request throttling
- Query optimization with `select_related()` and `prefetch_related()`
- OpenAPI 3 schema generation
- Interactive Swagger UI and ReDoc
- Automated permission, throttling, and versioning tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Programming language |
| Django 5.2 | Web framework |
| Django REST Framework | REST API development |
| django-filter | Query parameter filtering |
| drf-spectacular | OpenAPI schema and documentation |
| SQLite | Local development database |
| Django ORM | Database operations |
| pytest | Testing tooling |
| pytest-django | Django integration |
| Schemathesis | Schema-based API testing tooling |
| Ruff | Code linting |
| uv | Dependency management |

## Project Structure

```text
bookstore_api/
├── manage.py
├── pyproject.toml
├── schema.yml
├── README.md
├── catalog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── test_throttling.py
│   ├── test_versioning.py
│   ├── throttles.py
│   ├── urls.py
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
└── reviews/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── views.py
    └── migrations/
        ├── __init__.py
        └── 0001_initial.py
```

Generated `.hypothesis/` and `.schemathesis/` directories are excluded from the documented source structure because they contain testing artifacts rather than application code.

## Application Architecture

```text
                 HTTP Client
                      |
                      v
               Django URL Router
                      |
                      v
            Django REST Framework
                      |
          +-----------+-----------+
          |                       |
          v                       v
    AuthorViewSet            BookViewSet
          |                       |
          v                       v
    AuthorSerializer         BookSerializer
          |                       |
          |                 ReviewSerializer
          |                       |
          +-----------+-----------+
                      |
                      v
                  Django ORM
                      |
                      v
                SQLite Database
```

### Application Responsibilities

**catalog**

Manages authors and books, API routing, serializers, permissions, filtering, search, ordering, and throttling.

**reviews**

Defines the review model and serializer used for nested book review operations.

**config**

Contains Django settings, root URL routing, and OpenAPI documentation configuration.

## Database Models

The application uses three primary models.

### Author

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `name` | CharField | Author name |
| `email` | EmailField | Unique email address |

### Book

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `title` | CharField | Book title |
| `description` | TextField | Optional description |
| `author` | ForeignKey | Related author |
| `price` | DecimalField | Book price |
| `created_at` | DateTimeField | Creation timestamp |

### Review

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `book` | ForeignKey | Related book |
| `reviewer` | CharField | Reviewer name |
| `rating` | PositiveSmallIntegerField | Review rating |
| `comment` | TextField | Optional review comment |
| `created_at` | DateTimeField | Creation timestamp |

### Database Relationships

```text
Author
  |
  | One-to-Many
  v
Book
  |
  | One-to-Many
  v
Review
```

One author can have multiple books, and one book can have multiple reviews.

## API Versioning

The project uses Django REST Framework's `URLPathVersioning`.

Configuration:

```python
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": (
        "rest_framework.versioning.URLPathVersioning"
    ),
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    "VERSION_PARAM": "version",
}
```

The version is included in the API URL.

Supported version:

```text
/api/v1/
```

The test suite verifies that `/api/v1/books/` is accessible and that `/api/v2/books/` is rejected.

## API Endpoints

### Authors

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/authors/` | List authors |
| POST | `/api/v1/authors/` | Create an author |
| GET | `/api/v1/authors/{id}/` | Retrieve an author |
| PUT | `/api/v1/authors/{id}/` | Replace an author |
| PATCH | `/api/v1/authors/{id}/` | Partially update an author |
| DELETE | `/api/v1/authors/{id}/` | Delete an author |

### Books

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/books/` | List books |
| POST | `/api/v1/books/` | Create a book |
| GET | `/api/v1/books/{id}/` | Retrieve a book |
| PUT | `/api/v1/books/{id}/` | Replace a book |
| PATCH | `/api/v1/books/{id}/` | Partially update a book |
| DELETE | `/api/v1/books/{id}/` | Delete a book |

### API Documentation

| Endpoint | Purpose |
|---|---|
| `/api/schema/` | Generated OpenAPI schema |
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc documentation |
| `/admin/` | Django administration |

The application does not expose a standalone review endpoint. Reviews are included in book serialization and can be managed through nested book writes.

## API Request Examples

### Create an Author

**POST** `/api/v1/authors/`

```json
{
  "name": "Robert Martin",
  "email": "robert@example.com"
}
```

### Create a Book

**POST** `/api/v1/books/`

Requires an authenticated staff user.

```json
{
  "title": "Clean Architecture",
  "description": "A book about software architecture.",
  "author": 1,
  "price": "499.00",
  "reviews": [
    {
      "reviewer": "Alex",
      "rating": 5,
      "comment": "Excellent book."
    }
  ]
}
```

The `author` value must reference an existing author.

### Example Book Representation

An illustrative serialized response:

```json
{
  "id": 1,
  "title": "Clean Architecture",
  "description": "A book about software architecture.",
  "author": 1,
  "price": "499.00",
  "created_at": "2026-11-16T10:00:00Z",
  "reviews": [
    {
      "id": 1,
      "reviewer": "Alex",
      "rating": 5,
      "comment": "Excellent book.",
      "created_at": "2026-11-16T10:00:00Z"
    }
  ]
}
```

The IDs and timestamps above are illustrative.

## Nested Review Serialization

The `BookSerializer` includes:

```python
reviews = ReviewSerializer(
    many=True,
    required=False,
)
```

This enables books to be represented with their related reviews.

### Nested Creation

When creating a book, the serializer:

1. Extracts nested review data.
2. Creates the book.
3. Creates associated reviews.
4. Returns the created book.

### Nested Updates

When updating a book, the serializer:

1. Updates book fields.
2. Checks whether review data was supplied.
3. Deletes existing reviews if review data is present.
4. Creates the supplied replacement reviews.

**Important:** Nested review updates use replacement semantics, not individual review patching. Sending a `reviews` list replaces the existing collection; omitting `reviews` leaves the collection unchanged.

### Atomic Operations

Both serializer methods use:

```python
@transaction.atomic
```

This groups the book and review database writes within a transaction.

If an exception causes the transaction to roll back, the grouped database changes are not committed.

## Review Validation

The `ReviewSerializer` validates ratings between 1 and 5.

```python
def validate_rating(self, value):
    if not 1 <= value <= 5:
        raise serializers.ValidationError(
            "Rating must be between 1 and 5."
        )
    return value
```

This validation is applied through the serializer, including nested review writes.

## Filtering, Searching, and Ordering

The Book API supports three query capabilities.

### Filter by Author

```http
GET /api/v1/books/?author=1
```

### Search Books

```http
GET /api/v1/books/?search=django
```

Searchable fields:

- Book title
- Book description
- Author name

### Order Books

Ascending price:

```http
GET /api/v1/books/?ordering=price
```

Descending price:

```http
GET /api/v1/books/?ordering=-price
```

Supported ordering fields:

- `price`
- `created_at`
- `title`

The Author API also supports searching by author name and email address.

## API Permissions

The project uses Django REST Framework permission classes to control access.

### Global Permissions

```python
"DEFAULT_PERMISSION_CLASSES": [
    "rest_framework.permissions.IsAuthenticatedOrReadOnly",
]
```

This permits anonymous read operations while requiring authentication for write operations by default.

### Custom Book Permissions

The Book API uses:

```python
permission_classes = [IsStaffOrReadOnly]
```

The custom permission permits:

- Anonymous users to read books
- Authenticated users to read books
- Staff users to create, update, and delete books

Regular authenticated users cannot modify books.

### Permission Matrix

| User Type | Read Authors | Modify Authors | Read Books | Modify Books |
|---|---|---|---|---|
| Anonymous | Yes | No | Yes | No |
| Authenticated non-staff | Yes | Yes | Yes | No |
| Authenticated staff | Yes | Yes | Yes | Yes |

The Author API uses the global permission policy rather than the custom staff-only policy.

## API Throttling

The project configures global throttling and stricter Book API throttles.

### Global Throttle Rates

| Client Type | Limit |
|---|---|
| Anonymous | 100 requests/hour |
| Authenticated | 1000 requests/hour |

### Book API Throttle Rates

| Client Type | Limit |
|---|---|
| Anonymous | 5 requests/minute |
| Authenticated | 10 requests/minute |

The Book API uses:

```python
throttle_classes = [
    BookAnonThrottle,
    BookUserThrottle,
]
```

Requests exceeding the configured throttle rate may receive:

```http
HTTP/1.1 429 Too Many Requests
```

Throttling is intended to reduce excessive API usage, but DRF's built-in throttles should not be treated as a complete security or denial-of-service defense.

## Database Query Optimization

The Book ViewSet optimizes related-object retrieval.

```python
queryset = (
    Book.objects
    .select_related("author")
    .prefetch_related("reviews")
    .order_by("id")
)
```

### select_related()

Retrieves the book's related author through a SQL join.

### prefetch_related()

Retrieves related reviews using additional queries and associates them with books.

These techniques help reduce unnecessary database queries when serializing related data.

## OpenAPI Documentation

The application uses `drf-spectacular` to generate an OpenAPI schema.

### Swagger UI

```text
http://127.0.0.1:8000/api/docs/
```

### ReDoc

```text
http://127.0.0.1:8000/api/redoc/
```

### OpenAPI Schema

```text
http://127.0.0.1:8000/api/schema/
```

The repository also contains a generated `schema.yml` file describing the API's paths, request bodies, response schemas, and authentication mechanisms.

### Generate the Schema

```powershell
uv run python manage.py spectacular --file schema.yml
```

### Validate the Schema

```powershell
uv run python manage.py spectacular --validate
```

## Installation and Setup

### 1. Navigate to the Project

From the repository root:

```powershell
cd day22\bookstore_api
```

### 2. Install Dependencies

Python 3.11+ and `uv` are required.

```powershell
uv sync --group dev
```

### 3. Apply Database Migrations

```powershell
uv run python manage.py migrate
```

### 4. Create a Superuser

```powershell
uv run python manage.py createsuperuser
```

### 5. Start the Development Server

```powershell
uv run python manage.py runserver
```

### 6. Open the API Documentation

```text
http://127.0.0.1:8000/api/docs/
```

Use Swagger UI to explore the available endpoints.

## Automated Testing

The project contains Django test cases for permissions, throttling, and versioning.

### Run All Tests

```powershell
uv run python manage.py test
```

### Run Catalog Tests

```powershell
uv run python manage.py test catalog
```

### Permission Tests

The test suite checks:

- Anonymous users can read books.
- Anonymous users cannot create books.
- Regular authenticated users cannot create books.
- Staff users can create books.

### Throttling Tests

The anonymous Book API throttle test checks that:

- Five requests are permitted.
- The sixth request receives HTTP 429.

### Versioning Tests

The tests check that:

- The v1 Book API endpoint is accessible.
- An unsupported v2 API version is rejected.

The provided source contains seven explicit test methods across these three areas.

## Schema-Based Testing

Schemathesis is included in the development dependencies for API testing against an OpenAPI specification.

The project includes the generated `schema.yml` file and local Schemathesis testing artifacts.

Schemathesis can be used to explore API behavior against the documented schema. Its presence in the dependencies does not by itself establish a passing schema-based test run.

## Code Quality and Verification

Run the following checks:

```powershell
uv run python manage.py check
uv run python manage.py test
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py spectacular --validate
uv run ruff check .
```

## Security Considerations

The project demonstrates several API security controls:

- Authentication-aware write permissions
- Staff-only book modifications
- Anonymous and authenticated request throttling
- Serializer-level review validation
- Atomic nested database writes
- Restricted API versions

### Production Limitations

The current project uses development settings and requires additional hardening before public deployment.

Recommended improvements include:

1. Move the Django secret key into an environment variable.
2. Disable debug mode in production.
3. Configure trusted hosts and HTTPS.
4. Use a production database where appropriate.
5. Configure shared caching for throttling across multiple application instances.
6. Review authorization requirements for author modification.
7. Add stronger authentication and abuse protection where needed.
8. Expand automated tests for nested writes and invalid input.
9. Add production logging and monitoring.
10. Run Django deployment security checks.

## Learning Outcomes

Through Day 22, I explored:

1. REST API development with Django REST Framework.
2. CRUD endpoints using `ModelViewSet`.
3. Router-based API URL configuration.
4. URL path API versioning.
5. Model serializers.
6. Nested serializer operations.
7. Atomic database writes.
8. Serializer validation.
9. Query filtering, searching, and ordering.
10. Custom API permissions.
11. Anonymous and authenticated request throttling.
12. Query optimization for related objects.
13. OpenAPI schema generation.
14. Swagger UI and ReDoc documentation.
15. Automated API permission tests.
16. Rate-limit and versioning tests.
17. Schema-based API testing tooling.

---

**Day 22 | 30 Days of Backend Development**

**Author:** YashKhadse01