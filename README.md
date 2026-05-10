# TaskFlow

A modern, multi-user task manager with a Kanban board, drag-and-drop, dark mode, Pomodoro timer, analytics, and more. Built with Python Flask + SQLite + vanilla HTML/CSS/JS.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-green) ![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey) ![License](https://img.shields.io/badge/License-MIT-purple)

---

## Demo Account

| Email | Password |
|---|---|
| `admin@test.com` | `admin123` |

---

## Features

- **Kanban Board** — drag-and-drop tasks across To Do / In Progress / Done columns
- **Task Management** — create, edit, delete tasks with title, description, due date, priority, category, and time estimate
- **Categories** — color-coded labels per user
- **Task Templates** — one-click task creation from reusable templates (8 built-in defaults)
- **List View** — filterable, sortable table view of all tasks
- **Calendar View** — due dates visualized on a monthly calendar (FullCalendar)
- **Analytics** — completion rate, status/priority charts, 14-day activity graph, time tracked
- **Pomodoro Timer** — floating 25/5 min timer widget with task linking and time logging
- **Light & Dark Mode** — toggle persisted in localStorage, respects system preference
- **Multi-user Auth** — session-based login with secure password hashing (pbkdf2:sha256)
- **CSRF Protection** — all forms and AJAX mutations protected via Flask-WTF

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 + Flask 3 |
| Database | SQLite via Flask-SQLAlchemy |
| Auth | Flask-Login |
| Forms & CSRF | Flask-WTF |
| Frontend | Vanilla HTML5, CSS3, ES6+ JS |
| Drag & Drop | SortableJS (CDN) |
| Calendar | FullCalendar (CDN) |
| Charts | Chart.js (CDN) |

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/aihunter9892/taskmaster_basic.git
cd taskmaster_basic
```

### 2. Install dependencies

```bash
pip install flask flask-sqlalchemy flask-login flask-wtf email-validator werkzeug
```

### 3. Run the app

```bash
python run.py
```

App runs at **http://127.0.0.1:5000**

The demo account (`admin@test.com` / `admin123`) is created automatically on first run.

### Run on a different port

```bash
python run.py --port 5002
```

---

## Running Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v
pytest tests/ --cov=app   # with coverage
```

19 unit tests covering auth and task CRUD, ownership enforcement, and reordering.

---

## Project Structure

```
taskmaster_basic/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # SQLAlchemy models
│   ├── config.py            # Config class
│   ├── auth/                # Login, register, logout
│   ├── tasks/               # All task, category, template routes
│   ├── static/
│   │   ├── css/             # theme.css (tokens), main.css (styles)
│   │   └── js/              # theme.js, dragdrop.js, timer.js
│   └── templates/
│       ├── base.html
│       ├── auth/
│       └── tasks/           # dashboard, list, calendar, analytics, templates
├── tests/                   # pytest suite
├── run.py                   # Entry point + DB seeding
└── requirements.txt
```

---

## Default Credentials (for testing)

```
Email:    admin@test.com
Password: admin123
```

You can register additional accounts at `/register`.

---

## License

MIT
