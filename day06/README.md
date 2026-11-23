# Day 06 — PostgreSQL E-Commerce Database and Query Optimization

## Project Overview

Day 06 of my 30-Day Backend Development Roadmap focuses on PostgreSQL, relational database design, SQL queries, database indexing, and performance optimization.

I developed an **E-Commerce Database** to understand how backend applications store, manage, retrieve, and analyze business data.

## Technologies Used

- PostgreSQL 18
- SQL
- psql
- VS Code
- Windows PowerShell

## Learning Objectives

- Understand the difference between SQL and PostgreSQL.
- Design relational database tables.
- Implement primary keys and foreign keys.
- Use database constraints to maintain data integrity.
- Write SQL queries using joins, aggregation, subqueries, and CTEs.
- Understand SQL window functions.
- Create database indexes.
- Analyze query performance using `EXPLAIN (ANALYZE, BUFFERS)`.

## SQL vs PostgreSQL

| SQL | PostgreSQL |
|---|---|
| A language used to interact with relational databases | A relational database management system |
| Provides commands such as SELECT, INSERT, UPDATE, and DELETE | Stores, manages, and retrieves database records |
| Supported by multiple database systems | Implements SQL and provides additional database features |

**SQL is the language, while PostgreSQL is the database system.**

## Database Architecture

The database consists of five tables:

| Table | Responsibility |
|---|---|
| customers | Stores customer details |
| products | Stores product details, pricing, and inventory |
| orders | Stores customer orders |
| order_items | Stores products purchased in each order |
| payments | Stores payment information |

The tables use primary keys, foreign keys, UNIQUE, NOT NULL, and CHECK constraints to maintain data integrity.

## Project Structure

```text
day06/
├── ecommerce_db/
│   ├── schema.sql
│   ├── seed.sql
│   ├── queries.sql
│   └── indexes.sql
├── ecommerce_project/
│   ├── schema.sql
│   ├── seed.sql
│   ├── queries.sql
│   ├── indexes.sql
│   ├── benchmark.sql
│   └── README.md
└── README.md
```

## SQL Query Implementation

I practiced 25 SQL queries covering:

- SELECT, WHERE, ORDER BY, LIMIT
- COUNT, SUM, AVG
- GROUP BY and HAVING
- INNER JOIN and LEFT JOIN
- Subqueries and common table expressions
- Window functions using DENSE_RANK
- Customer spending and monthly revenue reporting

## Database Indexing

Three indexes were implemented:

1. `idx_products_category_price` — Optimizes category-based product filtering and price ordering.
2. `idx_orders_customer_date` — Supports customer order history queries.
3. `idx_payments_completed` — Supports completed-payment reporting using a partial covering index.

Actual performance depends on the query planner, table size, and data distribution.

## Performance Benchmarking

The project includes three benchmarking experiments using separate tables containing 100,000 records each.

1. Customer order history lookup
2. Product catalog filtering and sorting
3. Completed-payment revenue aggregation

I used `EXPLAIN (ANALYZE, BUFFERS)` to examine query execution plans, execution times, and buffer usage before and after indexing.

## How to Run

**Prerequisites:** PostgreSQL installed and a database named `ecommerce_db` created.

Navigate to the project directory:

```powershell
cd day06\ecommerce_project
```

Execute the SQL scripts:

```powershell
psql -U postgres -h 127.0.0.1 -d ecommerce_db -W -v ON_ERROR_STOP=1 -f .\schema.sql
psql -U postgres -h 127.0.0.1 -d ecommerce_db -W -v ON_ERROR_STOP=1 -f .\seed.sql
psql -U postgres -h 127.0.0.1 -d ecommerce_db -W -v ON_ERROR_STOP=1 -f .\queries.sql
psql -U postgres -h 127.0.0.1 -d ecommerce_db -W -v ON_ERROR_STOP=1 -f .\indexes.sql
psql -U postgres -h 127.0.0.1 -d ecommerce_db -W -v ON_ERROR_STOP=1 -P pager=off -f .\benchmark.sql
```

Review the scripts before rerunning them on an existing database.

## Real-World Applications

This project demonstrates database concepts used in:

- E-commerce platforms
- Product and inventory management
- Order management systems
- Payment processing and reporting
- Sales analytics
- Backend API development

## Skills Demonstrated

PostgreSQL, SQL, relational database design, data integrity, SQL joins, aggregation, indexing, query optimization, and performance analysis.

## Future Improvements

- Integrate PostgreSQL with FastAPI.
- Build REST APIs for products and orders.
- Implement database migrations.
- Add automated integration tests.
- Introduce transaction-safe inventory updates.

## Conclusion

Day 06 helped me understand how relational databases support backend applications and how SQL indexing and query analysis can improve database performance.