# TaskFlow — Development Roadmap

> Last updated: 2026-05-10
> Stack: Python Flask + SQLite + Vanilla HTML/CSS/JS
> Repo: https://github.com/aihunter9892/taskmaster_basic

---

## Phase 1 — Core App ✅ COMPLETE

### Backend
- [x] Flask app factory (`create_app`) with SQLAlchemy, Flask-Login, Flask-WTF
- [x] Models: `User`, `Task`, `Category`, `TaskTemplate`, `TimeEntry`
- [x] Auth blueprint: `/register`, `/login`, `/logout`
- [x] Tasks blueprint: CRUD, reorder (PATCH), delete (DELETE)
- [x] Category CRUD
- [x] Task Templates — 8 built-in defaults, custom user templates, one-click "use"
- [x] Time logging endpoint (`/tasks/<id>/timer/log`)
- [x] Auto schema migration in `run.py` (adds new columns to existing DB safely)
- [x] DB seeding: demo user `admin@test.com` / `admin123` on first run
- [x] Unit tests — 19 tests covering auth + task CRUD, ownership, reordering

### Frontend
- [x] Kanban board with drag-and-drop (SortableJS), 3 columns: To Do / In Progress / Done
- [x] All Tasks list view — filter by status/priority/search, sortable columns
- [x] Calendar view — FullCalendar.js, tasks shown on due date, color-coded by priority
- [x] Analytics dashboard — Chart.js, KPIs (total, completion rate, overdue, time tracked), 14-day activity chart, status/priority/category charts
- [x] Task Templates page — browse, create, delete templates
- [x] Quick Add strip on dashboard — one-click task creation from templates
- [x] Floating Pomodoro timer — 25/5/15 min modes, task linking, session counter, time logged to DB
- [x] Light / Dark mode toggle — persisted in localStorage, respects system preference
- [x] Responsive layout — collapses to single column on mobile

### Design
- [x] Airbnb-inspired aesthetic — generous whitespace, rounded cards, soft shadows
- [x] Pastel purple theme (`#A58FE8` primary, `#F5F0FF` background)
- [x] CSS custom properties throughout — no hardcoded hex in component styles

---

## Phase 2 — AI Features 🔜 NEXT

### 2.1 Gemini AI Email → Task Parser
- [ ] Add "Parse Email" button/modal on dashboard
- [ ] User pastes raw email text into textarea
- [ ] Send to Gemini API → extract: title, description, due date, priority, category suggestion
- [ ] Show parsed fields in a pre-filled "confirm task" form before saving
- [ ] Handle multi-task emails (one email → multiple tasks)
- [ ] Store Gemini API key in `.env` / environment variable

### 2.2 Smart Task Suggestions
- [ ] When creating a task, suggest priority and estimated time based on title keywords (local heuristics or Gemini)
- [ ] Auto-suggest category based on task title

---

## Phase 3 — Conversational Interface 🔮 FUTURE

### 3.1 Chatbot over Task Database
- [ ] Floating chat widget (bottom-right, above timer)
- [ ] Natural language queries: "What's due this week?", "How many tasks did I complete in April?"
- [ ] Natural language task creation: "Add a high priority bug fix for the login page due Friday"
- [ ] Context-aware: bot knows current user's tasks, categories, schedule
- [ ] Powered by Gemini or Claude API with function calling / tool use
- [ ] Conversation history stored per session

### 3.2 Weekly Digest Email
- [ ] Scheduled summary email every Monday morning
- [ ] Shows: tasks completed last week, overdue tasks, upcoming due dates
- [ ] Sent via SendGrid or SMTP

---

## Backlog (Unscheduled Ideas)

- [ ] Subtasks — nested checklist inside a task
- [ ] Task comments / notes thread
- [ ] File attachments on tasks
- [ ] Recurring tasks (daily / weekly / monthly)
- [ ] Team workspaces — share boards with other users
- [ ] Keyboard shortcuts (e.g. `N` = new task, `K` = kanban, `L` = list)
- [ ] Export tasks to CSV / JSON
- [ ] PWA support — installable on mobile, offline mode
- [ ] PostgreSQL migration path for production deployment
- [ ] Docker + docker-compose setup

---

## How to Resume in a New Session

1. App lives at `d:\inclass_demo\wclaudemd`
2. Run: `python run.py --port 5002`
3. Login: `admin@test.com` / `admin123`
4. Phase 1 is fully complete — do not rebuild existing features
5. Next task: **Phase 2.1 — Gemini AI Email Parser**
