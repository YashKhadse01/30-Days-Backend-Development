# Day 18 — Multi-Tenant Project Management API

A backend project management system built with **FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, role-based access control, and WebSockets**.

Part of my **30 Days of Backend Development** journey.

## Project Overview

This project demonstrates the architecture of a multi-tenant backend application in which multiple organizations share the same application while maintaining separate access to their resources.

Users can register, authenticate, create organizations, invite members, manage tasks, and receive real-time task notifications.

The project emphasizes tenant isolation, authorization, secure invitation handling, asynchronous database access, and maintainable backend architecture.

## Key Features

- User registration and JWT-based authentication
- Argon2 password hashing
- Organization creation and membership management
- Multi-tenant resource isolation
- Role-based access control (RBAC)
- Owner, Admin, and Member roles
- Secure organization invitations
- Hashed, expiring, single-use invitation tokens
- Organization-scoped task management
- Task assignment and status tracking
- Real-time task notifications using WebSockets
- Asynchronous PostgreSQL integration
- SQLAlchemy ORM models
- Alembic database migrations
- Automated integration and security tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend programming |
| FastAPI | REST API and WebSocket framework |
| PostgreSQL | Relational database |
| SQLAlchemy 2.x | Asynchronous ORM |
| asyncpg | Async PostgreSQL driver |
| Alembic | Database migrations |
| PyJWT | JWT authentication |
| pwdlib + Argon2 | Password hashing |
| Pydantic Settings | Environment configuration |
| Uvicorn | ASGI application server |
| pytest | Automated testing |
| pytest-asyncio | Async testing |
| HTTPX | API integration testing |
| pytest-cov | Coverage reporting |
| Ruff | Linting |
| uv | Dependency management |

## Project Structure

```text
multi-tenant-project-api/
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── README.md
├── alembic/
│   ├── env.py
│   ├── versions/
│   │   └── 73488b4bb9b2_create_initial_multi_tenant_tables.py
│   ├── README
│   └── script.py.mako
├── src/
│   └── multi_tenant_project_api/
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── main.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── entities.py
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── organizations.py
│       │   ├── invitations.py
│       │   └── tasks.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── organizations.py
│       │   ├── invitations.py
│       │   └── tasks.py
│       ├── security/
│       │   ├── __init__.py
│       │   └── auth.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── invitations.py
│       └── websocket/
│           ├── __init__.py
│           ├── manager.py
│           └── router.py
└── tests/
    ├── test_auth_integration.py
    ├── test_invitations_integration.py
    ├── test_invitation_edge_cases.py
    ├── test_invitation_rbac.py
    ├── test_organizations_integration.py
    ├── test_organization_owner.py
    ├── test_tasks_integration.py
    ├── test_task_crud_coverage.py
    ├── test_task_notifications.py
    ├── test_task_permissions.py
    ├── test_task_status_security.py
    ├── test_task_tenant_security.py
    └── test_websocket_integration.py
```

## System Architecture

```text
                    API Clients
                         |
                         v
                   FastAPI App
                         |
               JWT Authentication
                         |
                Organization RBAC
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
    Organizations    Invitations       Tasks
          |              |              |
          +--------------+--------------+
                         |
                  SQLAlchemy ORM
                         |
                       asyncpg
                         |
                     PostgreSQL

              Task Change Events
                         |
                         v
                 WebSocket Manager
                         |
                         v
             Organization Subscribers
```

The application uses a shared PostgreSQL database with organization-specific resource ownership and membership checks.

## Database Design

The application defines five primary database entities.

| Entity | Purpose |
|---|---|
| User | Stores user identity and password hashes |
| Organization | Represents an independent tenant |
| Membership | Connects users to organizations and assigns roles |
| Invitation | Manages invitations to join organizations |
| Task | Stores organization-specific work items |

### Entity Relationships

```text
User
  |
  +---- Creates ----> Organization
  |                       |
  |                       +---- Membership
  |                       |
  |                       +---- Invitation
  |                       |
  |                       +---- Task
  |
  +---- Belongs through Membership
```

UUID-based string identifiers are used for the primary entities.

The database schema includes unique membership constraints and a composite foreign key to help prevent assigning tasks to members of another organization.

## Installation and Setup

### 1. Navigate to the project

From the repository root:

```powershell
cd day18\multi-tenant-project-api
```

### 2. Install dependencies

Ensure Python 3.11+ and `uv` are installed.

```powershell
uv sync --group dev
```

### 3. Start PostgreSQL

A PostgreSQL server must be available.

For local development using Docker:

```powershell
docker run -d --name day18-postgres -e POSTGRES_USER=day18_user -e POSTGRES_PASSWORD=local_dev_password -e POSTGRES_DB=day18_db -p 5433:5432 postgres:16-alpine
```

If the container already exists and is stopped:

```powershell
docker start day18-postgres
```

These are example local development credentials only.

### 4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+asyncpg://day18_user:local_dev_password@127.0.0.1:5433/day18_db
JWT_SECRET=replace-with-a-long-random-secret
```

The application requires both `DATABASE_URL` and `JWT_SECRET`.

Generate a random JWT secret using Python:

```powershell
uv run python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Never commit `.env` or real credentials to Git.

### 5. Run database migrations

Apply the existing Alembic migrations:

```powershell
uv run alembic upgrade head
```

The Alembic configuration must point to the same PostgreSQL database.

### 6. Start the API

```powershell
uv run uvicorn multi_tenant_project_api.main:app --reload
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

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Authenticate and obtain JWT |
| GET | `/auth/me` | Retrieve authenticated user |

### Organizations

| Method | Endpoint | Description |
|---|---|---|
| POST | `/organizations` | Create an organization |
| GET | `/organizations` | List organizations belonging to the user |
| GET | `/organizations/{organization_id}` | Retrieve an accessible organization |

### Invitations

| Method | Endpoint | Description |
|---|---|---|
| POST | `/organizations/{organization_id}/invitations` | Invite a user |
| POST | `/invitations/accept` | Accept an invitation |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/organizations/{organization_id}/tasks` | Create task |
| GET | `/organizations/{organization_id}/tasks` | List tasks |
| GET | `/organizations/{organization_id}/tasks/{task_id}` | Retrieve task |
| PATCH | `/organizations/{organization_id}/tasks/{task_id}` | Update task details |
| PATCH | `/organizations/{organization_id}/tasks/{task_id}/status` | Change task status |
| PATCH | `/organizations/{organization_id}/tasks/{task_id}/assign` | Assign task |
| DELETE | `/organizations/{organization_id}/tasks/{task_id}` | Delete task |

### WebSockets

```text
/ws/organizations/{organization_id}
```

This endpoint provides organization-specific real-time task notifications.

## Authentication

The API uses JWT bearer authentication.

### Registration

**Endpoint:** `POST /auth/register`

A user registers with an email address and password. Passwords are hashed using Argon2 before storage.

### Login

**Endpoint:** `POST /auth/login`

After successful credential verification, the API issues a signed JWT access token.

The implementation uses:

- HS256 signing
- Subject (`sub`) claim
- Issued-at (`iat`) claim
- Expiration (`exp`) claim
- Access-token type validation
- Default 30-minute expiration

### Protected Requests

Authenticated endpoints require:

```http
Authorization: Bearer <access-token>
```

The application verifies the token, retrieves the corresponding user, and rejects inactive or missing accounts.

## Multi-Tenancy and Data Isolation

Multi-tenancy allows multiple organizations to operate independently within one application.

Each organization acts as a tenant.

The application enforces tenant isolation by checking organization membership and filtering organization-specific database queries.

For example, a task lookup requires both the task ID and organization ID to match.

```text
User A
  |
  +---- Organization A
             |
             +---- Tasks A

User B
  |
  +---- Organization B
             |
             +---- Tasks B
```

Users cannot access another organization's resources unless they have valid membership in that organization.

## Role-Based Access Control

The system defines three organization roles.

| Role | Responsibilities |
|---|---|
| Owner | Organization creator with management permissions |
| Admin | Organization management permissions |
| Member | Standard organization member |

### Permissions

| Operation | Owner | Admin | Member |
|---|---|---|---|
| View organization | Yes | Yes | Yes |
| View tasks | Yes | Yes | Yes |
| Create tasks | Yes | Yes | No |
| Edit task details | Yes | Yes | No |
| Assign tasks | Yes | Yes | No |
| Delete tasks | Yes | Yes | No |
| Invite users | Yes | Yes | No |
| Update task status | Yes | Yes | If assigned |

The creator of an organization automatically receives the Owner role.

## Secure Invitation Workflow

The invitation system allows Owners and Admins to invite users into an organization.

### Invitation Flow

```text
Owner / Admin
      |
      v
Create Invitation
      |
      v
Generate Secure Token
      |
      v
Store Token Hash
      |
      v
Invited User Authenticates
      |
      v
Submit Invitation Token
      |
      v
Validate Email + Expiration
      |
      v
Atomically Claim Invitation
      |
      v
Create Organization Membership
```

### Security Properties

- Tokens generated using Python's `secrets` module
- SHA-256 token hashes stored in PostgreSQL
- 24-hour invitation expiration
- Invitation tied to a specific email address
- One-time acceptance
- Atomic invitation claiming
- Duplicate membership prevention
- Role authorization for invitation creation

For development, the invitation creation endpoint returns the raw invitation token. Production systems should deliver invitations through a private channel instead.

## Task Management

Each task belongs to a specific organization.

Task attributes include:

- Unique identifier
- Organization identifier
- Title
- Optional description
- Status
- Assigned membership
- Creator
- Creation timestamp

### Task Statuses

```text
TODO
  |
  v
IN_PROGRESS
  |
  v
DONE
```

The supported status values are `todo`, `in_progress`, and `done`.

The current implementation accepts status updates from authorized managers or the assigned member; it does not enforce a strict sequential transition workflow.

### Task Assignment

Task assignments reference organization memberships rather than arbitrary users.

The application verifies that the assigned membership belongs to the same organization as the task.

This validation is also supported by a composite database foreign key.

## Real-Time WebSocket Notifications

The application supports real-time task events for connected organization members.

### WebSocket Authentication

Clients connect to:

```text
/ws/organizations/{organization_id}
```

The WebSocket handshake requires a bearer token in the `Authorization` header.

The server validates the JWT and verifies organization membership before accepting the connection.

### Supported Task Events

| Event | Trigger |
|---|---|
| `task.created` | Task created |
| `task.updated` | Task details updated |
| `task.status_changed` | Task status changed |
| `task.assigned` | Task assignment changed |
| `task.deleted` | Task deleted |

Example notification:

```json
{
  "type": "task.created",
  "organization_id": "<organization-id>",
  "task_id": "<task-id>",
  "actor_id": "<user-id>"
}
```

The connection manager groups active WebSocket connections by organization and broadcasts events to the relevant group.

The current implementation stores active connections in process memory.

## Database Migrations

The project uses Alembic to manage schema changes.

Apply migrations:

```powershell
uv run alembic upgrade head
```

Inspect migration status:

```powershell
uv run alembic current
```

Review migration history:

```powershell
uv run alembic history
```

The repository includes an initial migration for the multi-tenant database tables.

## Automated Testing

Run the complete test suite:

```powershell
uv run pytest -v
```

Generate coverage information:

```powershell
uv run pytest --cov=multi_tenant_project_api --cov-report=term-missing
```

Run Ruff:

```powershell
uv run ruff check .
```

The project includes 13 test modules covering:

- Authentication integration
- Organization creation and ownership
- Invitation workflows and edge cases
- Invitation role permissions
- Task CRUD operations
- Task permissions and status security
- Tenant isolation
- Task notifications
- WebSocket integration

The integration tests may require a configured test database. Use an isolated database rather than a production database when running tests.

## Security Considerations

- Use HTTPS and secure WebSocket connections in production.
- Protect JWT signing secrets.
- Store passwords using a modern password-hashing algorithm.
- Enforce tenant checks on every tenant-owned resource.
- Validate organization membership before task operations.
- Prevent cross-organization task assignments.
- Store invitation token hashes instead of raw tokens.
- Reject expired or previously accepted invitations.
- Use least-privilege role permissions.
- Keep database credentials outside version control.
- Use a dedicated test database for integration tests.
- Add centralized logging, monitoring, and audit trails for production.
- Consider a shared event broker for WebSocket delivery across multiple server instances.

The project is intended as a backend engineering demonstration. Production deployment requires additional operational and security hardening.

## Learning Outcomes

Through Day 18, I explored:

1. Multi-tenant backend architecture.
2. Organization-based data isolation.
3. JWT authentication and password hashing.
4. Role-based access control.
5. Secure invitation workflows.
6. Database-level tenant integrity constraints.
7. Asynchronous SQLAlchemy and PostgreSQL.
8. Alembic migrations.
9. Task management API design.
10. Real-time WebSocket communication.
11. Authorization and tenant security testing.
12. Modular FastAPI project organization.

---

**Day 18 | 30 Days of Backend Development**

**Author:** YashKhadse01