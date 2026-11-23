# Day 03 — Advanced Python: Decorators, Generators and Context Managers

## 30 Days of Backend Development

**Day:** 03  
**Main Project:** Reusable Python Decorators  
**Language:** Python 3.11+  
**Tools:** Python, uv, pytest, Git, GitHub

---

## 1. Overview

Day 03 explores advanced Python concepts used to create reusable, maintainable backend code.

The primary project is a collection of decorators that add execution-time monitoring, retry behavior, and time-limited caching to existing functions without modifying their internal implementations.

Additional practice files explore generators, iterators, context managers, and typing generics.

## 2. Learning Objectives

- Understand functions as first-class objects.
- Create decorators and nested wrapper functions.
- Use parameterized decorators.
- Preserve function metadata with `functools.wraps`.
- Implement retry logic for temporary failures.
- Measure execution time.
- Cache results with time-to-live expiration.
- Use `ParamSpec`, `TypeVar`, and `Callable` for typing.
- Explore generators and iterators.
- Practice context managers.
- Write automated unit tests with pytest.

## 3. Main Project — Reusable Decorator Library

The project contains three decorators.

### 3.1 Timed Decorator

**File:** `decorator_project/decorators.py`

The `@timed` decorator measures how long a function takes to execute.

It uses `time.perf_counter()` for elapsed-time measurement and a `finally` block so timing is reported even when the wrapped function raises an exception.

**Example:**

```python
@timed
def calculate_salary(basic_salary: int, bonus: int) -> int:
    return basic_salary + bonus
```

**Applications:** Performance monitoring, profiling, and identifying slow backend operations.

### 3.2 Retry Decorator

The `@retry` decorator repeats an operation when it raises `ConnectionError`.

Features:

- Configurable maximum number of attempts.
- Validation that `max_attempts` is at least 1.
- Retries only `ConnectionError`.
- Propagates an exception if the final attempt fails.
- Preserves the wrapped function's metadata.

**Example:**

```python
@retry(max_attempts=3)
def connect_to_server() -> str:
    ...
```

**Applications:** Network connections and transient external-service failures.

**Limitation:** The implementation does not include retry delays, exponential backoff, jitter, or idempotency handling.

### 3.3 Cache Decorator with TTL

The `@cache` decorator stores function results and reuses them while they remain valid.

Features:

- Configurable TTL.
- Cache hit and miss messages.
- Separate cache keys for different function arguments.
- Expiration using `time.monotonic()`.
- Validation that TTL is positive.

**Example:**

```python
@cache(ttl=3)
def calculate_square(number: int) -> int:
    return number * number
```

**Applications:** Avoiding repeated calculations and reducing unnecessary function executions.

**Limitations:** Arguments must be hashable; the cache is process-local, has no size limit, and is not designed as a distributed cache.

## 4. Project Structure

```text
day03/
├── decorator_project/
│   ├── decorators.py
│   ├── main.py
│   └── test_decorators.py
├── practice/
│   ├── cache_decorator.py
│   ├── contextlib_example.py
│   ├── context_manager.py
│   ├── decorator_arguments.py
│   ├── decorator_basics.py
│   ├── generator_basics.py
│   ├── generics_basics.py
│   ├── iterator_basics.py
│   ├── mypy_basics.py
│   ├── parameterized_decorator.py
│   ├── retry_decorator.py
│   └── timed_decorator.py
└── README.md
```

## 5. Key Python Concepts

| Concept | Purpose |
|---|---|
| Decorators | Extend function behavior without changing the original function |
| Closures | Preserve access to variables from enclosing scopes |
| `functools.wraps` | Preserve function metadata |
| `ParamSpec` | Preserve the wrapped function's parameter types |
| `TypeVar` | Represent generic return types |
| `time.perf_counter()` | Measure elapsed execution time |
| `time.monotonic()` | Track cache expiration using a monotonic clock |
| Generators | Produce values lazily |
| Iterators | Support sequential value retrieval |
| Context managers | Manage resource setup and cleanup |

## 6. Running the Project

From the repository root:

```powershell
cd day03\decorator_project
python main.py
```

The demonstration runs:

1. Execution-time monitoring for two functions.
2. A server connection simulation that succeeds on the third attempt.
3. A cached square calculation, including a repeated call and a call after TTL expiration.

The demonstration includes deliberate sleep delays.

## 7. Automated Testing

**Test file:** `decorator_project/test_decorators.py`

Ten pytest test functions are implemented.

| Test | Purpose |
|---|---|
| `test_timed_result` | Verify the original return value |
| `test_timed_function_name` | Verify function metadata preservation |
| `test_timed_output` | Verify execution-time output |
| `test_retry_success` | Verify recovery from temporary failures |
| `test_retry_failure` | Verify final failure propagation |
| `test_retry_invalid_attempts` | Reject invalid retry counts |
| `test_cache_hit` | Verify repeated calls reuse cached results |
| `test_cache_expiration` | Verify TTL expiration |
| `test_cache_different_arguments` | Verify separate cache keys |
| `test_cache_invalid_ttl` | Reject invalid TTL values |

### Run Tests

From the repository root:

```powershell
uv run --with pytest pytest day03/decorator_project/test_decorators.py -v
```

**Status:** Completed — 10/10 automated tests passed.
**Test execution time:** 0.19 seconds.

## 8. Real-World Applications

These concepts can be used in:

- Backend API performance monitoring.
- Database operation timing.
- External API retry handling.
- Reusable authentication and logging decorators.
- Caching expensive computations.
- File and database resource management.
- Memory-efficient data processing.

## 9. Engineering Considerations

The decorator project is a learning implementation rather than a production-ready resilience or caching framework.

For production use, additional considerations include:

- Exponential backoff and jitter for retries.
- Avoiding retries for non-idempotent operations.
- Cache eviction and memory limits.
- Thread and process safety.
- Structured logging and monitoring.
- Explicit handling of unhashable cache arguments.
- Additional tests for exceptions and edge cases.

## 10. Key Takeaways

Day 03 demonstrates how decorators can separate cross-cutting concerns from core business logic.

Instead of adding timing, retry, and caching logic to every function, these behaviors can be implemented once and reused.

The exercises also introduce Python features useful for building efficient, typed, and maintainable backend systems.

---

**Status:** Implementation complete; automated test results pending local verification.

**Next:** Day 04 — Continue the 30-day backend development roadmap.