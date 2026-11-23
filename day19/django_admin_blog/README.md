# Day 19 — Django Admin Blog

A full-stack blog application built with **Django 5.2**, demonstrating the Model–View–Template (MVT) architecture, class-based views, CRUD operations, authentication-based permissions, Django Admin customization, and automated testing.

Part of my **30 Days of Backend Development** journey.

## Project Overview

This project demonstrates how Django can be used to develop a database-driven web application with server-rendered templates and a built-in administration interface.

Users can browse published blog posts, while authenticated users can create posts and manage their own content.

Administrators can manage blog posts through a customized Django Admin interface, including bulk publishing and unpublishing actions.

## Key Features

- Django Model–View–Template architecture
- Blog post creation, listing, editing, and deletion
- Draft and published post statuses
- Automatic slug generation when a slug is omitted
- SEO-friendly, slug-based post URLs
- Author-based edit and delete permissions
- Login-required post creation
- Public listing of published posts
- Pagination with five posts per page
- Django ModelForms with validation
- CSRF-protected HTML forms
- Customized Django Admin interface
- Admin search and filtering
- Bulk publish and unpublish actions
- Separate development, testing, and production settings modules
- SQLite database and Django migrations
- Automated model, view, permission, and admin tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend programming |
| Django 5.2 | Web framework |
| SQLite | Development database |
| Django ORM | Database modeling and queries |
| Django Templates | Server-side HTML rendering |
| Django ModelForms | Form handling and validation |
| Django Admin | Content administration |
| Django TestCase | Automated testing |
| uv | Python dependency management |

## Project Structure

```text
django_admin_blog/
├── manage.py
├── pyproject.toml
├── README.md
├── blog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── test.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   └── templates/
│       └── blog/
│           ├── base.html
│           ├── post_list.html
│           ├── post_detail.html
│           ├── post_form.html
│           └── post_confirm_delete.html
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── production.py
│       └── testing.py
└── src/
    └── django_admin_blog/
        └── __init__.py
```

## Application Architecture

Django follows the Model–View–Template architectural pattern.

```text
                   Browser
                      |
                      v
                 URL Routing
                      |
                      v
              Class-Based Views
                      |
              +-------+-------+
              |               |
              v               v
         Django ORM       ModelForms
              |               |
              v               |
         SQLite Database      |
              |               |
              +-------+-------+
                      |
                      v
               Django Templates
                      |
                      v
                 HTML Response
```

### Architecture Components

**Models:** Define the database structure and business entities.

**Views:** Process HTTP requests and implement application behavior.

**Templates:** Render HTML pages using Django's template language.

**Forms:** Validate submitted data and create or update model instances.

**URL configuration:** Maps request paths to their corresponding views.

**Admin:** Provides an administrative interface for managing database records.

## Database Model

The application uses a `Post` model.

| Field | Description |
|---|---|
| `id` | Automatically generated primary key |
| `title` | Blog post title |
| `slug` | Unique URL-friendly identifier |
| `content` | Blog post content |
| `author` | Foreign key to Django's user model |
| `status` | Draft or published |
| `created_at` | Creation timestamp |
| `updated_at` | Last modification timestamp |
| `published_at` | Publication timestamp, if applicable |

### Publication Status

The application defines two statuses:

```text
DRAFT
  |
  | Publish
  v
PUBLISHED
  |
  | Unpublish
  v
DRAFT
```

New posts default to draft status.

The application also defines a database index on status and creation date to support common listing queries.

## Installation and Setup

### 1. Navigate to the project

From the repository root:

```powershell
cd day19\django_admin_blog
```

### 2. Install dependencies

Ensure Python 3.11+ and `uv` are installed.

```powershell
uv sync
```

### 3. Configure Django settings

The project provides separate settings modules:

```text
config.settings.development
config.settings.testing
config.settings.production
```

For local development, set the development settings module:

```powershell
$env:DJANGO_SETTINGS_MODULE = "config.settings.development"
```

This environment variable applies to the current PowerShell session.

### 4. Apply database migrations

```powershell
uv run python manage.py migrate
```

Django will create the local SQLite database and apply the existing migrations.

### 5. Create an administrator account

```powershell
uv run python manage.py createsuperuser
```

Follow the terminal prompts to configure the administrator account.

### 6. Start the development server

```powershell
uv run python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

The application uses Django's built-in development server. It is not intended for production hosting.

## Application Routes

| Method | URL | Purpose |
|---|---|---|
| GET | `/` | List published posts |
| GET | `/posts/<slug>/` | View a published post |
| GET, POST | `/posts/create/` | Create a post |
| GET, POST | `/posts/<slug>/edit/` | Edit an existing post |
| GET, POST | `/posts/<slug>/delete/` | Confirm and delete a post |
| GET | `/admin/` | Django administration interface |

Django Admin provides additional management routes internally.

## Blog CRUD Operations

### Create

Authenticated users can create blog posts through a Django ModelForm.

The application automatically associates each new post with the currently authenticated user.

When a post is created with published status, its publication timestamp is set.

### Read

The public post listing displays only published posts.

The list is ordered by publication date and creation date, with the newest posts appearing first.

The detail view also restricts access to published posts.

### Update

Only the original author can edit a post through the blog's update view.

When a draft is published, the publication timestamp is populated if it is not already present.

When a published post is moved back to draft, the publication timestamp is cleared.

### Delete

Only the original author can delete a post.

The application displays a confirmation page before deletion.

## Authentication and Authorization

Django's built-in authentication system is used to identify users.

The application uses two important class-based view mixins:

### LoginRequiredMixin

Restricts post creation, editing, and deletion to authenticated users.

Unauthenticated users are redirected toward the configured login URL.

### UserPassesTestMixin

Checks whether the authenticated user is the author of the requested post.

This prevents users from editing or deleting another author's content through the blog views.

The application does not define a custom login or registration page in its current URL configuration.

## Django Admin Customization

The `PostAdmin` class customizes Django's built-in administration interface.

### List Display

The admin list displays:

- Title
- Author
- Publication status
- Creation timestamp
- Publication timestamp

### Filtering

Administrators can filter posts by status, creation date, and author.

### Search

Administrators can search by title, content, and author username.

### Additional Features

- Automatic slug prepopulation from the title
- Read-only creation and update timestamps
- Pagination with 20 records per admin page
- Bulk publishing
- Bulk unpublishing

## Bulk Publishing and Unpublishing

The admin provides two custom actions.

### Publish Selected Posts

The action changes selected posts to published status and sets their publication timestamps.

### Move Selected Posts to Draft

The action changes selected posts to draft status and clears their publication timestamps.

These actions use Django ORM bulk updates.

## Django Templates

The application includes five templates.

| Template | Purpose |
|---|---|
| `base.html` | Shared page structure and navigation |
| `post_list.html` | Published post listing |
| `post_detail.html` | Individual post content |
| `post_form.html` | Post creation and editing |
| `post_confirm_delete.html` | Deletion confirmation |

The templates use Django's template inheritance system.

The base template provides the shared layout, while child templates populate content blocks.

### Template Features

- Conditional navigation based on authentication
- Post metadata and author display
- Post content rendering
- Pagination controls
- Conditional author edit/delete links
- CSRF protection for submitted forms
- Responsive CSS styling

## Pagination

The blog listing uses Django's `ListView` pagination:

```python
paginate_by = 5
```

This limits the public listing to five posts per page.

Example:

```text
/?page=1
/?page=2
/?page=3
```

The templates provide Previous and Next navigation links when applicable.

## Database Migrations

The project includes an initial migration:

```text
blog/migrations/0001_initial.py
```

Useful Django migration commands:

```powershell
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py showmigrations
```

Migrations allow database schema changes to be tracked and applied systematically.

## Automated Testing

The project uses Django's built-in `TestCase` framework.

Run the test suite:

```powershell
uv run python manage.py test
```

Run the blog application's tests:

```powershell
uv run python manage.py test blog
```

The `blog/tests.py` file contains tests for:

- Post creation
- String representation
- Automatic slug generation
- Absolute URL generation
- Published post visibility
- Draft post exclusion
- Published post detail access
- Anonymous user creation restrictions
- Authenticated post creation
- Author update permissions
- Unauthorized update prevention
- Author deletion permissions
- Unauthorized deletion prevention
- Admin bulk publishing
- Admin bulk unpublishing

The `blog/test.py` file is a separate placeholder and does not contain additional implemented tests.

## Django Settings Organization

The project separates configuration into multiple modules.

| Module | Purpose |
|---|---|
| `base.py` | Shared Django configuration |
| `development.py` | Development overrides |
| `testing.py` | Testing overrides |
| `production.py` | Production overrides |

The testing module disables debug mode and uses a faster MD5 password hasher for tests.

The production module currently disables debug mode but does not yet implement the environment-based secret, host, and database configuration described in its comment.

## Security Considerations

Django provides built-in mechanisms for several common web security concerns.

This project uses:

- CSRF middleware and form tokens
- Django authentication middleware
- Password validators
- Login-required views
- Author-based access restrictions
- Django's ORM for database access
- Clickjacking protection middleware
- Security middleware

### Production Hardening Required

Before deploying this project publicly:

1. Load `SECRET_KEY` from a secure environment variable.
2. Ensure `DEBUG = False`.
3. Configure `ALLOWED_HOSTS`.
4. Configure secure HTTPS and session settings.
5. Provide appropriate login and logout routes.
6. Configure static file handling.
7. Review the production database configuration.
8. Run Django's deployment checks.
9. Ensure secrets and local databases are excluded from version control.

The current application is intended as a development and learning project, not a production-ready deployment.

## Learning Outcomes

Through Day 19, I explored:

1. Django's Model–View–Template architecture.
2. Django models and database migrations.
3. Class-based generic views.
4. CRUD operations using Django.
5. ModelForms and form validation.
6. User authentication and authorization.
7. Author-based object permissions.
8. Draft and published content workflows.
9. Slug-based URL routing.
10. Django Admin customization.
11. Bulk administrative actions.
12. Pagination and template inheritance.
13. Automated Django testing.
14. Environment-specific Django settings.

---

**Day 19 | 30 Days of Backend Development**

**Author:** YashKhadse01