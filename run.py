from app import create_app, db
from app.models import User, TaskTemplate

app = create_app()

DEFAULT_TEMPLATES = [
    {'title': 'Morning Standup', 'priority': 'medium', 'estimated_minutes': 15, 'emoji': '☀️', 'description': 'Daily team sync — share progress, blockers, and plan for the day.'},
    {'title': 'Code Review', 'priority': 'medium', 'estimated_minutes': 45, 'emoji': '🔍', 'description': 'Review open pull requests and leave constructive feedback.'},
    {'title': 'Email Triage', 'priority': 'low', 'estimated_minutes': 30, 'emoji': '📧', 'description': 'Process inbox to zero — reply, delegate, or archive.'},
    {'title': 'Team Meeting', 'priority': 'medium', 'estimated_minutes': 60, 'emoji': '👥', 'description': 'Weekly team sync to align on priorities and updates.'},
    {'title': 'Deep Work Session', 'priority': 'high', 'estimated_minutes': 90, 'emoji': '🎯', 'description': 'Distraction-free focused work block. No meetings, no notifications.'},
    {'title': 'Bug Fix', 'priority': 'high', 'estimated_minutes': 120, 'emoji': '🐛', 'description': 'Investigate, reproduce, and fix a reported bug.'},
    {'title': 'Write Documentation', 'priority': 'low', 'estimated_minutes': 60, 'emoji': '📝', 'description': 'Write or update technical documentation or README.'},
    {'title': 'Weekly Planning', 'priority': 'high', 'estimated_minutes': 30, 'emoji': '📅', 'description': 'Review last week and plan priorities for the upcoming week.'},
]


def migrate_schema() -> None:
    """Add columns/tables missing in an existing database without dropping data."""
    with app.app_context():
        from sqlalchemy import text, inspect
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        existing_task_cols = (
            {col['name'] for col in inspector.get_columns('task')}
            if 'task' in table_names else set()
        )
        alters = []
        if 'estimated_minutes' not in existing_task_cols:
            alters.append('ALTER TABLE task ADD COLUMN estimated_minutes INTEGER')
        if 'completed_at' not in existing_task_cols:
            alters.append('ALTER TABLE task ADD COLUMN completed_at DATETIME')
        if alters:
            with db.engine.connect() as conn:
                for sql in alters:
                    try:
                        conn.execute(text(sql))
                        conn.commit()
                    except Exception:
                        pass
        db.create_all()


def seed_database() -> None:
    with app.app_context():
        if not User.query.filter_by(email='admin@test.com').first():
            user = User(username='admin', email='admin@test.com')
            user.set_password('admin123')
            db.session.add(user)
            db.session.flush()
            for t in DEFAULT_TEMPLATES:
                db.session.add(TaskTemplate(user_id=user.id, is_default=True, **t))
            db.session.commit()
            print('✓ Demo user created: admin@test.com / admin123')

        # Seed default templates for any user who has none yet
        for user in User.query.all():
            if not TaskTemplate.query.filter_by(user_id=user.id).first():
                for t in DEFAULT_TEMPLATES:
                    db.session.add(TaskTemplate(user_id=user.id, is_default=True, **t))
                db.session.commit()
                print(f'✓ Seeded templates for {user.username}')


migrate_schema()
seed_database()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    app.run(debug=True, port=args.port)
