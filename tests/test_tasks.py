import json
from app.models import Task, Category


def test_dashboard_shows_only_current_user_tasks(auth_client, test_user, second_user, db):
    own_task = Task(user_id=test_user.id, title='My Task', priority='low', status='todo', position=0)
    other_task = Task(user_id=second_user.id, title='Not Mine', priority='low', status='todo', position=0)
    db.session.add_all([own_task, other_task])
    db.session.commit()

    res = auth_client.get('/')
    assert b'My Task' in res.data
    assert b'Not Mine' not in res.data


def test_create_task_valid_payload(auth_client, db, test_user):
    res = auth_client.post('/tasks', data={
        'title': 'New Task',
        'priority': 'high',
        'status': 'todo',
        'category_id': 0,
    }, follow_redirects=True)
    assert res.status_code == 200
    assert Task.query.filter_by(user_id=test_user.id, title='New Task').first() is not None


def test_create_task_missing_title_shows_error(auth_client):
    res = auth_client.post('/tasks', data={
        'title': '',
        'priority': 'medium',
        'status': 'todo',
        'category_id': 0,
    }, follow_redirects=True)
    assert res.status_code == 200


def test_edit_task_owner_can_update(auth_client, sample_task, db):
    res = auth_client.post(f'/tasks/{sample_task.id}/edit', data={
        'title': 'Updated Title',
        'priority': 'high',
        'status': 'in_progress',
        'category_id': 0,
    }, follow_redirects=True)
    assert res.status_code == 200
    db.session.refresh(sample_task)
    assert sample_task.title == 'Updated Title'
    assert sample_task.status == 'in_progress'


def test_edit_task_non_owner_gets_404(client, sample_task, second_user, db):
    client.post('/login', data={'email': 'other@example.com', 'password': 'password123'})
    res = client.get(f'/tasks/{sample_task.id}/edit')
    assert res.status_code == 404


def test_delete_task_owner_succeeds(auth_client, sample_task, db):
    res = auth_client.delete(f'/tasks/{sample_task.id}')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['success'] is True
    assert db.session.get(Task, sample_task.id) is None


def test_delete_task_non_owner_returns_403(client, sample_task, second_user):
    client.post('/login', data={'email': 'other@example.com', 'password': 'password123'})
    res = client.delete(f'/tasks/{sample_task.id}')
    assert res.status_code == 403


def test_reorder_tasks_updates_position_and_status(auth_client, test_user, db):
    t1 = Task(user_id=test_user.id, title='T1', priority='low', status='todo', position=0)
    t2 = Task(user_id=test_user.id, title='T2', priority='low', status='todo', position=1)
    db.session.add_all([t1, t2])
    db.session.commit()

    res = auth_client.patch('/tasks/reorder',
        data=json.dumps({'tasks': [
            {'id': t1.id, 'position': 0, 'status': 'in_progress'},
            {'id': t2.id, 'position': 1, 'status': 'in_progress'},
        ]}),
        content_type='application/json',
    )
    assert res.status_code == 200
    db.session.refresh(t1)
    assert t1.status == 'in_progress'


def test_create_category_valid(auth_client, test_user, db):
    res = auth_client.post('/categories', data={'name': 'Work', 'color': '#FF385C'}, follow_redirects=True)
    assert res.status_code == 200
    assert Category.query.filter_by(user_id=test_user.id, name='Work').first() is not None


def test_delete_category_non_owner_returns_403(client, sample_category, second_user):
    client.post('/login', data={'email': 'other@example.com', 'password': 'password123'})
    res = client.delete(f'/categories/{sample_category.id}')
    assert res.status_code == 403
