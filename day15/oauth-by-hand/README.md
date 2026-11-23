# Day 15 — Google OAuth 2.0 From Scratch

A Python backend authentication project implementing the **Google OAuth 2.0 Authorization Code Flow with PKCE**, OpenID Connect identity verification, account linking, and application session management using FastAPI.

Part of my **30 Days of Backend Development** journey.

## Project Overview

This project explores how third-party authentication works internally without depending on a high-level OAuth integration framework.

The application redirects users to Google for authentication, handles the OAuth callback, exchanges the authorization code for tokens, verifies the Google ID token, links or registers a local user account, and creates an application session.

## Key Features

- Google OAuth 2.0 Authorization Code Flow
- PKCE using SHA-256 (S256)
- Cryptographically generated OAuth state and nonce
- Browser-binding cookie for OAuth state validation
- Authorization code exchange using HTTPX
- Google ID token verification
- Google account registration and linking
- Application session creation and revocation
- HTTP-only session cookies
- Bearer-token authentication support
- Same-origin checks for cookie-authenticated logout
- Automated authentication and security tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend development |
| FastAPI | API framework |
| Uvicorn | ASGI server |
| HTTPX | Asynchronous HTTP requests |
| Cryptography | Cryptographic operations |
| python-dotenv | Environment configuration |
| pytest | Automated testing |
| pytest-asyncio | Asynchronous testing |
| pytest-cov | Test coverage |
| uv | Dependency management |

## Project Structure

```text
oauth-by-hand/
├── pyproject.toml
├── README.md
├── src/
│   └── oauth_by_hand/
│       ├── __init__.py
│       ├── main.py
│       ├── authorization.py
│       ├── pkce.py
│       ├── oauth_state.py
│       ├── token_exchange.py
│       ├── google_identity.py
│       ├── account_linking.py
│       └── sessions.py
└── tests/
    ├── test_account_linking.py
    ├── test_full_oauth_flow.py
    ├── test_google_callback.py
    ├── test_google_identity.py
    ├── test_oauth_security.py
    ├── test_sessions.py
    └── test_token_exchange.py
```

## OAuth Authentication Flow

```text
User
  |
  v
GET /auth/google/login
  |
  v
Generate PKCE Verifier, Challenge,
OAuth State, Nonce and Browser Binding
  |
  v
Redirect to Google Authorization
  |
  v
User Authenticates with Google
  |
  v
GET /auth/google/callback
  |
  v
Validate State and Browser Binding
  |
  v
Exchange Authorization Code
Using PKCE Verifier
  |
  v
Verify Google ID Token and Nonce
  |
  v
Register or Link Google Account
  |
  v
Create Application Session
  |
  v
Set HTTP-only Session Cookie
  |
  v
Access Protected API Endpoints
```

## Installation and Setup

### 1. Navigate to the project

From the repository root:

```powershell
cd day15\oauth-by-hand
```

### 2. Install dependencies

Ensure Python 3.11+ and `uv` are installed.

```powershell
uv sync --group dev
```

### 3. Configure Google OAuth credentials

Create a `.env` file in the project directory:

```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/auth/google/callback
```

Configure a Google OAuth client in Google Cloud Console and register the exact redirect URI used by the application.

The application uses `http://127.0.0.1:8000/auth/google/callback` as its default callback URI.

**Security:** Never commit `.env`, client secrets, access tokens, or refresh tokens to GitHub.

### 4. Start the application

```powershell
uv run uvicorn oauth_by_hand.main:app --reload
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

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Health check |
| GET | `/auth/google/login` | Begin Google OAuth authentication |
| GET | `/auth/google/callback` | Complete Google OAuth authentication |
| GET | `/auth/me` | Retrieve authenticated user profile |
| POST | `/auth/logout` | Revoke the current session |

## Authentication Workflow

### Step 1 — Start Google Login

Open the following URL in a browser:

```text
http://127.0.0.1:8000/auth/google/login
```

The application generates a PKCE verifier and challenge, OAuth state, nonce, and browser-binding value.

It then redirects the browser to Google's authorization endpoint.

If the Google client ID is missing, the endpoint returns HTTP 503.

### Step 2 — Google Authorization Callback

After Google authentication, the browser returns to:

```text
GET /auth/google/callback
```

The callback processes the authorization code and state.

The application validates the stored OAuth context, exchanges the authorization code for tokens, verifies the Google ID token, and registers or links the Google account.

### Step 3 — Application Session

On successful authentication, the application creates a session and sets an HTTP-only cookie named:

```text
app_session
```

The cookie is configured with:

- `HttpOnly=True`
- `SameSite=Lax`
- `Max-Age=1800`
- `Secure=True` when the configured redirect URI uses HTTPS

The application also removes the temporary OAuth browser-binding cookie.

### Step 4 — Access the Authenticated Profile

**Endpoint:** `GET /auth/me`

The endpoint accepts an authenticated application session through the session cookie or an HTTP bearer token.

Example response structure:

```json
{
  "user_id": "<user-id>",
  "email": "user@example.com",
  "google_linked": true
}
```

### Step 5 — Logout

**Endpoint:** `POST /auth/logout`

The application revokes the authenticated session and deletes the session cookie.

When authenticating through a cookie, the logout endpoint also requires same-origin verification using request headers.

## Understanding PKCE

Proof Key for Code Exchange (PKCE) protects the OAuth authorization code flow against certain authorization code interception attacks.

The application generates a random code verifier and derives an S256 challenge:

```text
code_challenge =
BASE64URL(SHA256(code_verifier))
```

The challenge is included in the Google authorization request.

The original verifier is submitted during the token exchange, allowing Google to validate that the token request corresponds to the original authorization flow.

## OAuth State and Nonce

**State** helps protect the authorization flow against request forgery and login CSRF attacks.

**Nonce** binds the OpenID Connect identity token to the authentication request.

The application also associates OAuth state with a temporary browser-binding cookie.

These mechanisms serve different security purposes and complement PKCE.

## Account Linking and Sessions

The application separates account management and session management into dedicated modules:

- `account_linking.py` — Google identity registration and account association
- `sessions.py` — Application session creation, lookup, and revocation
- `google_identity.py` — Google ID token verification

The current FastAPI application accesses user records through the account-linking module.

## Automated Testing

Run all tests:

```powershell
uv run pytest -v
```

Run tests with coverage:

```powershell
uv run pytest --cov=oauth_by_hand --cov-report=term-missing
```

The test suite contains dedicated files for account linking, OAuth flows, callbacks, Google identity verification, security, sessions, and token exchange.

## Security Considerations

- Keep Google client credentials outside version control.
- Use HTTPS for deployed OAuth callbacks.
- Validate OAuth state and browser binding.
- Use PKCE with S256.
- Validate Google ID token signatures and relevant claims.
- Verify the expected nonce.
- Protect session cookies and authentication tokens.
- Apply appropriate CSRF protections to state-changing endpoints.
- Use secure, shared session storage when scaling beyond a single development process.
- Review account-linking rules to prevent unauthorized account takeover.
- Avoid logging authorization codes, access tokens, and ID tokens.

**Note:** This is an educational implementation. Production deployment requires additional security review, operational controls, and persistent session/account storage.

## Learning Outcomes

Through Day 15, I explored:

1. OAuth 2.0 Authorization Code Flow.
2. Google authentication integration.
3. PKCE verifier and challenge generation.
4. OAuth state and nonce validation.
5. Asynchronous authorization code exchange.
6. OpenID Connect identity verification.
7. Third-party account registration and linking.
8. Application session and cookie management.
9. Authentication and CSRF security considerations.
10. Automated testing of OAuth workflows.

---

**Day 15 | 30 Days of Backend Development**

**Author:** YashKhadse01