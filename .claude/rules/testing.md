# Testing Conventions

## Framework
- Use **pytest** (no unittest)
- Test files live in `tests/`; mirror the app structure (`test_auth.py`, `test_tasks.py`)

## Fixtures (conftest.py)
- `app` fixture: creates a fresh Flask app configured for testing (`TESTING=True`, in-memory SQLite)
- `client` fixture: provides a test client from the app fixture
- `auth_client` fixture: test client with a logged-in user pre-seeded
- `db` fixture: provides the database session; rolls back after each test

```python
# Example fixture pattern
@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

## What to Test
### Auth (`test_auth.py`)
- Register: valid data creates user; duplicate email/username returns error
- Login: valid credentials redirect to dashboard; invalid credentials show error
- Logout: clears session, redirects to login
- Protected routes return 302 redirect when unauthenticated

### Tasks (`test_tasks.py`)
- Create: valid payload creates task; missing required fields return 400
- Edit: owner can edit; another user cannot (403)
- Delete: owner can delete; non-owner gets 403; JSON response returned
- Reorder: PATCH `/tasks/reorder` updates position field correctly
- Dashboard: only authenticated user's tasks are shown

## Rules
- Each test function tests exactly one behavior
- Test names follow `test_<action>_<condition>` pattern (e.g., `test_login_invalid_password`)
- No hardcoded sleep or time.sleep — mock datetime where needed
- Aim for ≥ 80% coverage on `app/` (run `pytest --cov=app tests/`)
- Do not test Flask internals or SQLAlchemy internals — test your own logic only
