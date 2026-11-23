# Day 20 — Django ORM Lab

A database engineering laboratory built with **Django 5.2**, focused on advanced ORM operations, relational database modeling, SQL query optimization, custom managers, transactions, signals, and performance testing.

Part of my **30 Days of Backend Development** journey.

## Project Overview

The Django ORM Lab explores how Django interacts with relational databases and how ORM queries can be optimized for better application performance.

Instead of focusing on conventional CRUD functionality, this project investigates database relationships, query execution, the N+1 query problem, aggregation, subqueries, transaction handling, and model signals.

The project includes reproducible experiments, a sample-data generator, a browser-based performance comparison, and automated tests that verify SQL query counts.

## Key Features

- Relational database modeling
- One-to-many and many-to-many relationships
- Custom Django QuerySets and managers
- Advanced filtering with `Q` expressions
- Database-side calculations with `F` expressions
- Aggregation using `Count`, `Avg`, `Min`, and `Max`
- Correlated subqueries with `Subquery` and `OuterRef`
- N+1 query problem demonstrations
- Query optimization using `select_related()`
- Query optimization using `prefetch_related()`
- Review count optimization using annotations
- SQL query counting and comparison
- Atomic database transactions
- Database-side stock updates
- `select_for_update()` experimentation
- Django `post_save` and `post_delete` signals
- Custom management command for generating sample data
- Django Debug Toolbar integration
- Automated ORM optimization tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Programming language |
| Django 5.2 | Web framework and ORM |
| SQLite | Local relational database |
| Django ORM | Database operations |
| Django Debug Toolbar | SQL inspection and debugging |
| Django TestCase | Automated database testing |
| pytest | Additional testing tooling |
| pytest-django | Django integration with pytest |
| Ruff | Code linting |
| uv | Dependency management |

## Project Structure

```text
django_orm_lab/
├── manage.py
├── pyproject.toml
├── README.md
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── orm_lab/
│   ├── __init__.py
│   ├── admin.py
│   ├── advanced_queries.py
│   ├── apps.py
│   ├── managers.py
│   ├── models.py
│   ├── performance_views.py
│   ├── query_experiments.py
│   ├── signals.py
│   ├── signal_experiments.py
│   ├── transaction_experiments.py
│   ├── views.py
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── seed_data.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   └── tests/
│       ├── __init__.py
│       └── test_orm.py
└── src/
    └── django_orm_lab/
        └── __init__.py
```

## Database Architecture

The application models a simplified book catalog with five entities.

| Model | Purpose |
|---|---|
| Author | Stores author information |
| Publisher | Stores publishing organizations |
| Category | Classifies books |
| Book | Main entity containing book details |
| Review | Stores book reviews and ratings |

### Entity Relationships

```text
Author ───────┐
              │ Many-to-Many
              v
             Book ───────── Publisher
              │              ForeignKey
              │
              ├───────────── Category
              │              Many-to-Many
              │
              └───────────── Review
                             One-to-Many
```

A book can have multiple authors, multiple categories, and multiple reviews.

Each book belongs to one publisher, and each review belongs to one book.

## Database Models

### Author

Stores an author's name and unique email address.

### Publisher

Stores the publisher's name and country.

### Category

Stores a unique category name.

### Book

The primary model contains:

- Title
- Authors
- Publisher
- Categories
- Price
- Stock
- Publication date
- Creation timestamp

The model uses a custom `BookManager` for reusable queries.

### Review

Stores:

- Related book
- Reviewer name
- Rating
- Optional comment
- Creation timestamp

## Custom QuerySets and Managers

The project defines a `BookQuerySet` with reusable query methods.

### In-Stock Books

```python
Book.objects.in_stock()
```

Returns books with stock greater than zero.

### Affordable Books

```python
Book.objects.affordable(max_price=350)
```

Returns books whose prices do not exceed the specified limit.

### Recently Published Books

```python
Book.objects.recently_published(days=30)
```

Returns books published within the specified number of days.

These methods can be reused and chained with other Django QuerySet operations.

## Advanced ORM Queries

### Q Expressions

`Q` objects allow complex conditions using logical operators.

The project demonstrates:

- OR conditions
- AND conditions
- Negated conditions

Example:

```python
from django.db.models import Q

books = Book.objects.filter(
    Q(price__lt=310) | Q(stock__gt=80)
)
```

### F Expressions

`F` expressions reference database fields directly.

The project demonstrates comparisons between fields and calculated annotations.

```python
from django.db.models import F

books = Book.objects.annotate(
    projected_stock=F("stock") + 10
)
```

This example calculates projected stock without modifying stored values.

### Subquery and OuterRef

The project retrieves the latest review associated with each book using correlated subqueries.

The result includes annotations for:

- Latest reviewer
- Latest review rating

### Aggregation

The project calculates:

- Total number of books
- Average book price
- Minimum book price
- Maximum book price
- Number of reviews per book

These operations demonstrate database-level calculations using Django's aggregation API.

## Understanding the N+1 Query Problem

The N+1 problem occurs when an application first retrieves a collection of records and then executes additional queries to load related data for each record.

For example:

```python
books = Book.objects.all()

for book in books:
    print(book.publisher.name)
```

Accessing each publisher may cause an additional database query.

The project compares unoptimized and optimized query patterns.

### select_related()

Used for single-valued relationships, such as ForeignKey relationships.

```python
books = Book.objects.select_related("publisher")
```

Django retrieves related publisher information through a SQL join.

### prefetch_related()

Used for many-to-many and reverse foreign-key relationships.

```python
books = Book.objects.prefetch_related(
    "authors",
    "categories",
    "reviews",
)
```

Django retrieves related records in separate queries and associates them in Python.

### Combined Optimization

```python
books = (
    Book.objects
    .select_related("publisher")
    .prefetch_related(
        "authors",
        "categories",
        "reviews",
    )
)
```

This combines both techniques to optimize loading several relationships.

## SQL Performance Experiments

The `query_experiments.py` module contains five comparisons.

| Experiment | Optimization |
|---|---|
| Publisher relationship | `select_related()` |
| Author relationship | `prefetch_related()` |
| Review relationship | `prefetch_related()` |
| Multiple relationships | Combined select and prefetch |
| Review counts | `annotate(Count("reviews"))` |

The experiments use Django's `CaptureQueriesContext` to measure executed SQL queries.

### Expected Query Counts in Automated Tests

The test suite explicitly verifies the following query counts against its five-book fixture.

| Operation | Expected SQL queries |
|---|---:|
| Publisher with `select_related()` | 1 |
| Authors with `prefetch_related()` | 2 |
| Categories with `prefetch_related()` | 2 |
| Reviews with `prefetch_related()` | 2 |
| Combined relationship optimization | 4 |
| Annotated review counts | 1 |

These are assertions in the automated tests, not benchmark results from a production database.

## Database Transactions

The `transaction_experiments.py` module demonstrates atomic database operations.

The experiment:

1. Retrieves an existing book.
2. Records its original stock.
3. Starts an atomic transaction.
4. Uses `select_for_update()` to request row locking.
5. Checks available stock.
6. Decrements stock using an `F` expression.
7. Commits the transaction.
8. Restores the original stock for repeatable experimentation.

Example:

```python
from django.db import transaction
from django.db.models import F

with transaction.atomic():
    Book.objects.filter(
        pk=book_id,
        stock__gt=0,
    ).update(stock=F("stock") - 1)
```

The actual project uses additional checks and a `select_for_update()` call.

**Database note:** The configured database is SQLite. Its locking behavior differs from PostgreSQL, and `select_for_update()` does not provide the same row-level locking guarantees on SQLite.

## Django Signals

The project uses Django model signals to observe review lifecycle events.

| Signal | Event |
|---|---|
| `post_save` | Review created |
| `post_save` | Review updated |
| `post_delete` | Review deleted |

Signal handlers record events through Python's logging module.

The handlers are registered when `OrmLabConfig.ready()` imports the signals module.

The project also includes a signal experiment that creates, updates, and deletes a review while observing the logger calls.

## Sample Data Generation

The custom management command creates sample records for ORM experiments.

Run:

```powershell
uv run python manage.py seed_data
```

The command is designed to populate:

| Entity | Sample records |
|---|---:|
| Authors | 10 |
| Publishers | 5 |
| Categories | 5 |
| Books | 50 |
| Reviews | 150 |

The command uses `get_or_create()` to reduce duplicate records on repeated execution.

It also runs inside an atomic database transaction.

## Installation and Setup

### 1. Navigate to the project

From the main repository:

```powershell
cd day20\django_orm_lab
```

### 2. Install dependencies

Python 3.11+ and `uv` are required.

```powershell
uv sync --group dev
```

The development dependencies include Django Debug Toolbar, pytest, pytest-django, and Ruff.

### 3. Apply migrations

```powershell
uv run python manage.py migrate
```

This creates the local SQLite database and applies the existing migrations.

### 4. Generate sample data

```powershell
uv run python manage.py seed_data
```

### 5. Start the Django development server

```powershell
uv run python manage.py runserver
```

Open the performance experiment:

```text
http://127.0.0.1:8000/performance/
```

## Performance Comparison Interface

The project provides a browser-accessible performance view.

### Unoptimized

```text
http://127.0.0.1:8000/performance/?optimized=0
```

### Optimized

```text
http://127.0.0.1:8000/performance/?optimized=1
```

Both pages display book information, including publisher, authors, categories, and review counts.

The optimized version uses `select_related()` and `prefetch_related()`.

The interface is intended for comparison alongside Django Debug Toolbar rather than as a production-facing catalog.

## Django Debug Toolbar

Django Debug Toolbar is included in the development dependencies and configured in the application's settings.

When debug mode is enabled, the toolbar URLs are available under:

```text
/__debug__/
```

The toolbar can help inspect:

- Executed SQL queries
- Query execution time
- Duplicate queries
- Request information
- Database activity

Use the performance endpoints to compare SQL behavior with and without relationship optimization.

## Running ORM Experiments

The experiment functions can be executed through Django's shell.

Start the shell:

```powershell
uv run python manage.py shell
```

### Advanced Expressions

```python
from orm_lab.advanced_queries import run_advanced_queries

run_advanced_queries()
```

### Subqueries and Aggregation

```python
from orm_lab.advanced_queries import run_subquery_aggregation

run_subquery_aggregation()
```

### Relationship Query Comparisons

```python
from orm_lab.query_experiments import (
    compare_publisher_queries,
    compare_author_queries,
    compare_review_queries,
    compare_combined_queries,
    compare_review_count_queries,
)

compare_publisher_queries()
compare_author_queries()
compare_review_queries()
compare_combined_queries()
compare_review_count_queries()
```

### Transaction Experiment

```python
from orm_lab.transaction_experiments import demonstrate_transaction

demonstrate_transaction()
```

### Signal Experiment

```python
from orm_lab.signal_experiments import demonstrate_signals

demonstrate_signals()
```

Run the seed command first so these experiments have records to process.

## Automated Testing

The project contains a dedicated Django ORM test suite.

Run:

```powershell
uv run python manage.py test
```

Run only the ORM tests:

```powershell
uv run python manage.py test orm_lab.tests
```

The tests cover:

- Book record counts
- ForeignKey query optimization
- Many-to-many prefetching
- Reverse foreign-key prefetching
- Combined query optimization
- Review count annotations
- Custom manager filtering

Several tests use Django's `assertNumQueries()` to verify SQL query counts.

## Code Quality

Run Ruff:

```powershell
uv run ruff check .
```

Check Django configuration:

```powershell
uv run python manage.py check
```

Check for pending model migrations:

```powershell
uv run python manage.py makemigrations --check --dry-run
```

## Security and Limitations

This project is a development laboratory and is not configured for public production deployment.

Current limitations include:

- Hardcoded Django secret key
- Debug mode enabled
- SQLite as the local database
- Django Debug Toolbar enabled
- No production-specific settings
- Transaction locking behavior dependent on the database backend
- Performance measurements intended for educational experimentation

Before deploying a related application publicly, configure secure environment variables, disable debug mode, review database concurrency guarantees, restrict debugging tools, and validate all user-generated output.

## Learning Outcomes

Through Day 20, I explored:

1. Django ORM fundamentals and relational modeling.
2. ForeignKey and ManyToMany relationships.
3. Custom QuerySets and model managers.
4. Advanced filtering with `Q` expressions.
5. Database-side calculations with `F` expressions.
6. Aggregation and annotations.
7. Correlated subqueries using `Subquery` and `OuterRef`.
8. Identifying and reducing N+1 queries.
9. `select_related()` and `prefetch_related()`.
10. SQL query counting and performance experiments.
11. Atomic transactions and stock updates.
12. Database concurrency considerations.
13. Django model signals.
14. Custom management commands.
15. Automated ORM performance testing.
16. Database inspection with Django Debug Toolbar.

---

**Day 20 | 30 Days of Backend Development**

**Author:** YashKhadse01