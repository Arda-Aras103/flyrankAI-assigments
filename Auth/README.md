# A4: Auth · Login & Protect

Secure FastAPI API that handles user sign up, log in, and log out with
Supabase Auth as the Identity Provider. Protected routes verify JSON Web
Tokens (JWT) on every request through a reusable guard.

## Setup

1. Create a free project at [supabase.com](https://supabase.com).
2. In the dashboard, open **Authentication → Sign In / Providers → Email**
   and turn **Confirm email** off (practice project only).
3. Copy `.env.example` to `.env` and fill in your values from
   **Project Settings → API**:

```env
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
PORT=8000
```

Never use the `service_role` key here.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn supabase python-dotenv
uvicorn main:app --port 8000 --reload
```

API: http://localhost:8000
Swagger UI: http://localhost:8000/docs

## Endpoints

| Method | Endpoint           | Description                    | Auth required |
| ------ | ------------------ | ------------------------------ | ------------- |
| POST   | `/auth/signup`     | Create a new user account      | No            |
| POST   | `/auth/login`      | Log in and receive a JWT       | No            |
| POST   | `/auth/logout`     | End the session                | Yes           |
| GET    | `/public/info`     | Public, open data              | No            |
| GET    | `/protected/profile` | Current user's profile       | Yes           |
| GET    | `/protected/dashboard` | Dashboard for logged-in users | Yes        |

Protected routes expect the header `Authorization: Bearer <access_token>`.

## Example

```bash
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## Notes

- Passwords are never stored by this app. Supabase hashes them.
- JWTs are stateless. After logout the server still accepts the token until
  it expires (about one hour by default). Instant revocation would need an
  extra mechanism such as a token blacklist or a shorter access token lifetime.
