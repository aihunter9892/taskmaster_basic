# Code Style Guidelines

## Python
- Follow PEP 8; max line length 100 characters
- Use type hints on all function signatures
- Use f-strings for string formatting; no % or .format()
- Blueprint pattern for all route modules — no routes on the app object directly
- One model per file is acceptable; keep models.py under 200 lines, split if needed
- No unused imports; remove dead code immediately

## Flask Conventions
- Use the app factory pattern (`create_app()` in `app/__init__.py`)
- Config lives in a `Config` class, never hardcoded in routes
- All form handling uses Flask-WTF with CSRF protection enabled
- Return JSON responses for AJAX endpoints (reorder, delete); return rendered templates otherwise

## HTML / CSS
- Semantic HTML5 elements (`<main>`, `<section>`, `<article>`, `<nav>`, `<header>`)
- BEM-lite naming: `.card`, `.card__title`, `.card--high-priority`
- All colors via CSS custom properties defined in `theme.css` — never hardcode hex values in `main.css`
- No inline styles; no `!important` except inside theme overrides
- JS is vanilla ES6+; no jQuery, no external JS libraries except for drag-and-drop if needed (SortableJS is allowed)

## JavaScript
- Use `const` by default, `let` when reassignment is needed; never `var`
- Async operations use `fetch` + `async/await`; handle errors explicitly
- DOM manipulation only after `DOMContentLoaded`
- No global variables; wrap in modules or IIFEs

## File Naming
- Python files: `snake_case.py`
- Templates: `snake_case.html`
- CSS/JS: `kebab-case.css`, `kebab-case.js`
