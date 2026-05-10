# Security Requirements

## Authentication
- Passwords hashed with `werkzeug.security.generate_password_hash` (pbkdf2:sha256, salt_length=16)
- Never store or log plaintext passwords
- Session secret key loaded from environment variable `SECRET_KEY`; never hardcoded
- Flask-Login `@login_required` on every task route — no exceptions

## Authorization
- Every task query must filter by `user_id == current_user.id`; never fetch by task ID alone
- Return HTTP 403 (not 404) when a logged-in user tries to access another user's task
- Category ownership validated the same way as tasks

## CSRF
- Flask-WTF CSRF protection enabled globally (`WTF_CSRF_ENABLED = True`)
- AJAX mutation requests (DELETE, PATCH) must include the CSRF token in the `X-CSRFToken` header
- Token exposed to JS via a `<meta name="csrf-token">` tag in `base.html`

## Input Validation
- All form inputs validated server-side with Flask-WTF validators — client-side validation is UX only
- Task title: max 200 chars; description: max 2000 chars
- Due date must be a valid date; priority must be one of `low`, `medium`, `high`
- Reject unexpected fields; do not pass `**request.form` directly to model constructors

## Database
- Use SQLAlchemy ORM for all queries — no raw SQL string interpolation
- SQLite WAL mode enabled for local dev to reduce locking issues

## HTTP
- Set `Secure`, `HttpOnly`, `SameSite=Lax` on session cookie in production config
- No sensitive data in URL query parameters
- API error responses return JSON `{"error": "message"}` — never expose stack traces

## Dependencies
- Pin all versions in `requirements.txt`
- Do not add new dependencies without evaluating their security track record
