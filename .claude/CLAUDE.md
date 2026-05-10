# TaskFlow — CLAUDE.md

## Project Overview
TaskFlow is a multi-user task manager web application.
- **Backend:** Python 3 + Flask + SQLite (via Flask-SQLAlchemy)
- **Frontend:** Plain HTML + CSS (no framework), vanilla JS
- **Auth:** Flask-Login with session-based authentication
- **Design:** Airbnb-inspired, supports light and dark mode via CSS custom properties

## Directory Structure
```
wclaudemd/
├── .claude/
│   ├── CLAUDE.md
│   └── rules/
│       ├── code-style.md
│       ├── testing.md
│       └── security.md
├── app/
│   ├── __init__.py          # App factory, extensions init
│   ├── models.py            # SQLAlchemy models
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py        # /login, /register, /logout
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── routes.py        # CRUD + drag-and-drop order API
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css     # Design tokens, layout
│   │   │   └── theme.css    # Light/dark mode variables
│   │   └── js/
│   │       ├── dragdrop.js  # Drag-and-drop reordering
│   │       └── theme.js     # Theme toggle + persistence
│   └── templates/
│       ├── base.html        # Layout, nav, theme toggle
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       └── tasks/
│           ├── dashboard.html
│           ├── task_form.html
│           └── partials/
│               └── task_card.html
├── tests/
│   ├── conftest.py          # Pytest fixtures, test app factory
│   ├── test_auth.py
│   └── test_tasks.py
├── run.py                   # Entry point: `python run.py`
└── requirements.txt
```

## Models
```
User        id, username, email, password_hash
Task        id, user_id(FK), title, description, due_date,
            priority(low/medium/high), category, status, position, created_at
Category    id, user_id(FK), name, color
```

## Key Routes
| Method | Route | Description |
|--------|-------|-------------|
| GET/POST | `/register` | Register new user |
| GET/POST | `/login` | Login |
| GET | `/logout` | Logout |
| GET | `/` | Dashboard — task board |
| POST | `/tasks` | Create task |
| GET/POST | `/tasks/<id>/edit` | Edit task |
| DELETE | `/tasks/<id>` | Delete task |
| PATCH | `/tasks/reorder` | Update drag-and-drop order |

## Design Principles
- Airbnb aesthetic: generous whitespace, rounded cards, soft shadows
- CSS custom properties drive all colors — toggling `data-theme="dark"` on `<html>` switches the palette
- Theme preference stored in `localStorage`
- Responsive: mobile-first grid, collapses to single column below 768px

## Running Locally
```bash
pip install flask flask-sqlalchemy flask-login flask-wtf
python run.py
# App runs at http://127.0.0.1:5000
```

## Running Tests
```bash
pip install pytest
pytest tests/ -v
```

## Rules
- Code style: see [rules/code-style.md](rules/code-style.md)
- Testing: see [rules/testing.md](rules/testing.md)
- Security: see [rules/security.md](rules/security.md)
