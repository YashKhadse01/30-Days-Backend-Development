# Day 02 — Object-Oriented Programming in Python

## 30 Days of Backend Development

**Day:** 02  
**Topic:** Object-Oriented Programming (OOP)  
**Main Project:** Library Management System  
**Language:** Python 3.11+  
**Tools:** Python, uv, pytest, Git, GitHub

---

## 1. Overview

Day 02 focuses on understanding and applying Object-Oriented Programming principles in Python.

The main objective is to move beyond basic Python syntax and build reusable, maintainable code using classes, objects, interfaces, validation, and exception handling.

The practical implementation is a **Library Management System**, supported by individual exercises and automated tests.

## 2. Learning Objectives

- Understand classes, objects, constructors, and instance methods.
- Apply encapsulation and property-based validation.
- Implement Python special (dunder) methods.
- Use dataclasses and `__post_init__`.
- Understand inheritance and polymorphism.
- Work with abstract base classes (ABC).
- Explore structural typing using `Protocol`.
- Create custom exception hierarchies.
- Organize Python code into reusable modules.
- Write automated tests using pytest.

## 3. Project — Library Management System

The Library Management System demonstrates how OOP concepts can be applied to a practical software application.

### Implemented Components

**Book Model**

Defines book-related data and behavior, including validation and Python special methods.

**Library Repository**

Manages the book collection and provides operations for adding, finding, borrowing, and returning books.

**Interfaces**

Defines contracts for repository behavior and book display functionality.

**Custom Exceptions**

Provides application-specific errors for invalid library operations.

**Main Module**

Contains the application's entry point.

### Core Operations

- Add a book to the library.
- Find a book by ISBN.
- Borrow an available book.
- Return a borrowed book.
- Reject duplicate book entries.
- Handle missing books and invalid borrowing or return operations.

## 4. Project Structure

```text
day02/
├── library_management/
│   ├── exceptions.py
│   ├── interfaces.py
│   ├── library.py
│   ├── main.py
│   ├── models.py
│   ├── pyproject.toml
│   ├── README.md
│   └── src/
│       └── library_management/
│           └── __init__.py
├── practice/
│   ├── custom_exceptions.py
│   ├── dataclass_basics.py
│   ├── dunder_methods.py
│   ├── lesson5_abc.py
│   ├── lesson5_protocol.py
│   ├── oop_basics.py
│   └── properties.py
├── tests/
│   ├── test_library.py
│   └── test_models.py
├── test_models.py
├── requirements.txt
└── README.md
```

## 5. OOP Concepts Practiced

| Concept | Application |
|---|---|
| Classes and objects | Book and Library classes |
| Encapsulation | Controlled access to book attributes |
| Properties | Validation through getters and setters |
| Dunder methods | String representation, equality, hashing, and length |
| Dataclasses | Structured data models and post-initialization checks |
| Inheritance | Specialized book and library item examples |
| Abstract base classes | Defining required methods |
| Protocol | Structural interface contracts |
| Custom exceptions | Handling library-specific errors |
| Polymorphism | Common operations across different object types |

## 6. Testing

Automated tests are organized in the `tests/` directory, with an additional model test file at the Day 02 root.

The tests cover:

- Book creation and validation.
- Invalid page counts and prices.
- Equality, hashing, and special methods.
- Adding and finding books.
- Duplicate book handling.
- Borrowing and returning books.
- Error handling for invalid operations.
- Repository interface behavior.
- Application entry-point behavior.

## Testing

The project includes automated tests for Python OOP concepts
and Library Management System functionality.

### Run Tests

From the day02 directory:

```powershell
$env:PYTHONPATH = (Get-Location).Path
uv run --with pytest pytest tests/ test_models.py -v --import-mode=importlib
```

### Verified Results

- Tests passed: 40
- Tests failed: 0
- Warnings: 1 (RuntimeWarning from runpy)
- Execution time: 0.27 seconds

## 7. Important Python Concepts

### `__init__`

Initializes a new object.

### `__str__` and `__repr__`

Provide readable and developer-oriented object representations.

### `__eq__` and `__hash__`

Define object equality and hashing behavior.

### `__len__`

Allows custom objects to support Python's `len()` function.

### `@property`

Controls attribute access and supports validation.

### `@dataclass`

Reduces repetitive class initialization code.

### `ABC` and `@abstractmethod`

Define interfaces that subclasses must implement.

### `Protocol`

Supports structural typing based on available methods and attributes.

### Custom Exceptions

Make error handling more specific and maintainable.

## 8. Real-World Applications

The principles practiced in this project are useful for:

- Backend service architecture.
- Inventory management applications.
- E-commerce systems.
- Data models and business logic.
- Repository and service layers.
- API development.
- Enterprise application development.

## 9. Key Takeaways

Day 02 strengthened the foundation required to design modular backend applications.

The most important learning outcome was understanding how to separate data models, business operations, interfaces, exceptions, and tests rather than placing all functionality in one Python file.

These concepts will be reused throughout the remaining backend development roadmap.

---

**Status:** Implementation and test files available; current test results should be verified locally.

**Next:** Day 03 — Python Modules, Files, Exceptions, and Packaging.