from app.models import User


def test_register_valid_data_creates_user(client, db):
    res = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'securepass',
        'confirm_password': 'securepass',
    }, follow_redirects=True)
    assert res.status_code == 200
    assert User.query.filter_by(email='new@example.com').first() is not None


def test_register_duplicate_email_returns_error(client, test_user):
    res = client.post('/register', data={
        'username': 'anotheruser',
        'email': 'test@example.com',
        'password': 'securepass',
        'confirm_password': 'securepass',
    }, follow_redirects=True)
    assert b'already registered' in res.data


def test_register_duplicate_username_returns_error(client, test_user):
    res = client.post('/register', data={
        'username': 'testuser',
        'email': 'unique@example.com',
        'password': 'securepass',
        'confirm_password': 'securepass',
    }, follow_redirects=True)
    assert b'already taken' in res.data


def test_register_password_mismatch_returns_error(client):
    res = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'securepass',
        'confirm_password': 'different',
    }, follow_redirects=True)
    assert b'match' in res.data.lower()


def test_login_valid_credentials_redirects_to_dashboard(client, test_user):
    res = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123',
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Good' in res.data


def test_login_invalid_password_shows_error(client, test_user):
    res = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword',
    }, follow_redirects=True)
    assert b'Invalid email or password' in res.data


def test_login_unknown_email_shows_error(client):
    res = client.post('/login', data={
        'email': 'nobody@example.com',
        'password': 'password123',
    }, follow_redirects=True)
    assert b'Invalid email or password' in res.data


def test_logout_clears_session_and_redirects(auth_client):
    res = auth_client.get('/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b'Sign In' in res.data or b'sign in' in res.data.lower()


def test_dashboard_redirects_unauthenticated_user(client):
    res = client.get('/', follow_redirects=False)
    assert res.status_code == 302
    assert '/login' in res.headers['Location']
