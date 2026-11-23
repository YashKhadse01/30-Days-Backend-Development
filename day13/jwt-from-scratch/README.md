# Day 13 — JWT Authentication From Scratch

A Python project exploring the internal workings of **JSON Web Tokens (JWT)** through modular implementations of token encoding, decoding, cryptographic signatures, claims validation, refresh tokens, and token revocation.

Part of my **30 Days of Backend Development** journey.

## Project Overview

JWT is a compact, URL-safe token format commonly used to transmit claims between systems. JWTs are frequently used in authentication and authorization workflows.

This project focuses on understanding how JWTs work internally rather than relying entirely on a high-level JWT library.

## Project Structure

```text
jwt-from-scratch/
├── pyproject.toml
├── README.md
├── src/
│   └── jwt_from_scratch/
│       ├── __init__.py
│       ├── encoding.py
│       ├── hs256.py
│       ├── rs256.py
│       ├── jwt_decoder.py
│       ├── claims.py
│       ├── refresh.py
│       └── revocation.py
└── tests/
    ├── test_hs256.py
    ├── test_rs256.py
    ├── test_jwt_decoder.py
    ├── test_claims.py
    ├── test_refresh.py
    └── test_revocation.py
```

## Topics Covered

| Module | Purpose |
|---|---|
| `encoding.py` | JWT encoding and related data transformations |
| `hs256.py` | HMAC-SHA256 signing concepts |
| `rs256.py` | RSA-SHA256 signing concepts |
| `jwt_decoder.py` | Token decoding and verification |
| `claims.py` | JWT claims and validation |
| `refresh.py` | Refresh-token mechanisms |
| `revocation.py` | Token revocation concepts |

## Technology Stack

- **Language:** Python 3.11+
- **Cryptography:** `cryptography`
- **Package Manager:** `uv`
- **Testing:** `pytest`
- **Coverage:** `pytest-cov`
- **Build Backend:** `uv_build`

## Installation

### 1. Navigate to the project

```powershell
cd day13\jwt-from-scratch
```

### 2. Install dependencies

Ensure `uv` is installed, then run:

```powershell
uv sync --group dev
```

### 3. Run the test suite

```powershell
uv run pytest -v
```

### 4. Run tests with coverage

```powershell
uv run pytest --cov=jwt_from_scratch --cov-report=term-missing
```

## JWT Structure

A JWT typically contains three Base64URL-encoded components separated by periods:

```text
HEADER.PAYLOAD.SIGNATURE
```

**Header:** Describes the token type and signing algorithm.

**Payload:** Contains claims such as the subject, issuer, and expiration time.

**Signature:** Allows the recipient to verify the token's integrity and authenticity when the signing key is trusted.

JWT payloads are encoded, not encrypted. Sensitive information should not be stored in plaintext JWT claims.

## HS256 vs RS256

| Property | HS256 | RS256 |
|---|---|---|
| Cryptographic approach | Symmetric | Asymmetric |
| Signing key | Shared secret | RSA private key |
| Verification key | Shared secret | RSA public key |
| Typical use | Trusted systems sharing a secret | Systems separating signing and verification |

## Security Considerations

- Validate token signatures before trusting claims.
- Explicitly restrict accepted signing algorithms.
- Validate relevant claims such as expiration, issuer, and audience.
- Keep signing secrets and private keys secure.
- Use short-lived access tokens where appropriate.
- Protect refresh tokens against theft and replay.
- Treat revocation as a server-side security concern.

**Note:** This is an educational implementation. Production applications should use maintained, security-reviewed JWT libraries and carefully designed authentication flows.

## Testing

The project includes dedicated test modules covering:

- HS256 functionality
- RS256 functionality
- JWT decoding
- Claims handling
- Refresh-token behavior
- Revocation behavior

Tests can be executed using:

```powershell
uv run pytest -v
```

## Learning Outcomes

Through this project, I explored:

1. The structure and purpose of JSON Web Tokens.
2. Base64URL encoding and JWT serialization.
3. Symmetric and asymmetric token signatures.
4. Claims validation and token expiration concepts.
5. Access-token and refresh-token lifecycle management.
6. Token revocation and related security considerations.
7. Automated testing of authentication components.

---

**Day 13 | 30 Days of Backend Development**

**Author:** YashKhadse01