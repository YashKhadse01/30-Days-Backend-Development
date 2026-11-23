# Day 04 — Python Concurrency & Async Programming

## Overview

Day 04 of my 30-Day Backend Development roadmap focuses on Python concurrency, asynchronous programming, HTTP communication, and efficient execution of I/O-bound tasks.

The main project is an **Async API Data Aggregator** that retrieves users, posts, and comments concurrently from the JSONPlaceholder public REST API.

The project demonstrates how asynchronous programming can improve efficiency when an application needs to perform multiple independent network requests.

## Learning Objectives

- Understand sequential execution versus concurrent execution.
- Learn the fundamentals of threading and multiprocessing.
- Understand asynchronous programming using `asyncio`.
- Work with `async` and `await`.
- Perform asynchronous HTTP requests using `httpx`.
- Execute multiple independent requests using `asyncio.gather()`.
- Handle HTTP errors, request timeouts, and invalid response formats.
- Measure execution time using `time.perf_counter()`.
- Write automated tests using `pytest`.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11+ | Programming language |
| asyncio | Asynchronous task scheduling |
| HTTPX | Asynchronous HTTP requests |
| Requests | Synchronous HTTP practice |
| threading | Thread-based concurrency practice |
| multiprocessing | Process-based parallelism practice |
| pytest | Automated testing |
| pytest-cov | Test coverage reporting |
| uv | Dependency management |

## Project Structure

```text
day04/
├── README.md
├── pyproject.toml
├── uv.lock
├── concurrency_project/
│   ├── api_client.py
│   ├── main.py
│   ├── pyproject.toml
│   ├── README.md
│   └── test_api_client.py
└── practice/
    ├── asyncio_example.py
    ├── async_tasks.py
    ├── cpu_benchmark.py
    ├── httpx_example.py
    ├── multiprocessing_example.py
    ├── requests_example.py
    ├── sequential.py
    └── threading_example.py
```

## Main Project — Async API Data Aggregator

The application retrieves data from three REST API endpoints:

| Endpoint | Data |
|---|---|
| `/users` | Users |
| `/posts` | Posts |
| `/comments` | Comments |

Base URL: https://jsonplaceholder.typicode.com

### How It Works

1. The application starts an asynchronous event loop using `asyncio.run()`.
2. It creates an `httpx.AsyncClient` with a 10-second request timeout.
3. Three independent GET requests are scheduled using `asyncio.gather()`.
4. Each response is checked for HTTP errors.
5. The returned JSON is validated to ensure it is a list.
6. The application counts the records returned by each endpoint.
7. Results and total execution time are displayed.

### Architecture

```text
main.py
   |
   v
fetch_all_data()
   |
   v
httpx.AsyncClient
   |
   +---- GET /users
   |
   +---- GET /posts
   |
   +---- GET /comments
   |
   v
asyncio.gather()
   |
   v
Validate JSON responses
   |
   v
Count records
   |
   v
Display results and execution time
```

## Key Concepts

### 1. Sequential Execution

Tasks execute one after another. When a network request is waiting for a response, subsequent requests must wait.

### 2. Concurrent Execution

Multiple tasks can make progress during overlapping periods. This is useful when operations spend significant time waiting for network or disk I/O.

### 3. Asynchronous Programming

Python's `asyncio` allows coroutines to cooperate through an event loop.

The `await` keyword suspends the current coroutine while an awaitable operation progresses.

### 4. asyncio.gather()

`asyncio.gather()` schedules multiple awaitable operations and returns their results in the same order as the supplied awaitables.

In this project, it is used to request users, posts, and comments concurrently.

### 5. Threading vs Multiprocessing

Threading is useful for many I/O-bound operations. Multiprocessing allows CPU-intensive Python workloads to execute across separate processes.

### 6. HTTP Error Handling

The project uses `response.raise_for_status()` to detect unsuccessful HTTP responses.

It also handles `httpx.HTTPError` and `ValueError` at the application entry point.

## Installation

Navigate to the main project:

```powershell
cd day04\concurrency_project
```

Install dependencies:

```powershell
uv sync
```

## Run the Application

```powershell
uv run python main.py
```

The application prints the number of users, posts, and comments returned by the API, along with execution time.

An internet connection is required when running the application against the live JSONPlaceholder service.

## Testing

Run the automated tests:

```powershell
uv run pytest -v
```

Run the coverage report:

```powershell
uv run pytest --cov=api_client --cov-report=term-missing
```

### Recorded Results

According to the existing project README:

- 6 automated tests passed.
- 100% statement coverage was reported for `api_client.py`.

These are previously recorded project results, not a new test execution.

## Real-World Applications

- Aggregating data from multiple external APIs.
- Backend services that call independent microservices.
- Concurrent data collection and integration pipelines.
- Network-bound automation.
- API monitoring and reporting systems.

## Engineering Considerations

This project demonstrates foundational asynchronous programming. Production systems may additionally require:

- Retry policies with backoff.
- Concurrency limits.
- Structured logging.
- API authentication.
- Rate-limit handling.
- Observability and monitoring.

## Key Takeaways

Day 04 strengthened my understanding of concurrency, asynchronous HTTP communication, coroutine scheduling, error handling, and automated testing.

The main takeaway is that **concurrent I/O can reduce overall waiting time when several independent network operations are required**.

---

**Roadmap:** 30 Days of Backend Development  
**Day:** 04  
**Project:** Async API Data Aggregator  
**Status:** Completed — 6 tests passed, 100% statement coverage reported in the project README.