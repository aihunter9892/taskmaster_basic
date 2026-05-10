import pytest
from app import create_app, db as _db
from app.models import User, Task, Category


@pytest.fixture(scope='function')
def app():
    application = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret',
    })
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def test_user(app, db):
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def second_user(app, db):
    user = User(username='otheruser', email='other@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_client(client, test_user):
    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})
    return client


@pytest.fixture
def sample_task(app, db, test_user):
    task = Task(
        user_id=test_user.id,
        title='Sample Task',
        description='A test task',
        priority='medium',
        status='todo',
        position=0,
    )
    db.session.add(task)
    db.session.commit()
    return task


@pytest.fixture
def sample_category(app, db, test_user):
    cat = Category(user_id=test_user.id, name='Work', color='#FF385C')
    db.session.add(cat)
    db.session.commit()
    return cat
