from datetime import datetime, date, timezone, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.tasks import tasks_bp
from app.tasks.forms import TaskForm, TemplateForm
from app.models import Task, Category, TaskTemplate, TimeEntry


def _category_choices(user_id: int) -> list:
    cats = Category.query.filter_by(user_id=user_id).all()
    return [(0, 'No Category')] + [(c.id, c.name) for c in cats]


def _set_completed_at(task: Task, new_status: str) -> None:
    if new_status == 'done' and task.status != 'done':
        task.completed_at = datetime.now(timezone.utc)
    elif new_status != 'done' and task.status == 'done':
        task.completed_at = None


@tasks_bp.route('/')
@login_required
def dashboard():
    tasks_todo = Task.query.filter_by(user_id=current_user.id, status='todo').order_by(Task.position).all()
    tasks_in_progress = Task.query.filter_by(user_id=current_user.id, status='in_progress').order_by(Task.position).all()
    tasks_done = Task.query.filter_by(user_id=current_user.id, status='done').order_by(Task.position).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    templates = TaskTemplate.query.filter_by(user_id=current_user.id).order_by(TaskTemplate.is_default.desc(), TaskTemplate.id).all()

    task_form = TaskForm()
    task_form.category_id.choices = _category_choices(current_user.id)

    hour = datetime.now().hour
    greeting = 'morning' if hour < 12 else 'afternoon' if hour < 17 else 'evening'

    return render_template(
        'tasks/dashboard.html',
        tasks_todo=tasks_todo,
        tasks_in_progress=tasks_in_progress,
        tasks_done=tasks_done,
        categories=categories,
        templates=templates,
        task_form=task_form,
        today=date.today(),
        greeting=greeting,
    )


@tasks_bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    form = TaskForm()
    form.category_id.choices = _category_choices(current_user.id)
    if form.validate_on_submit():
        max_pos = db.session.query(db.func.max(Task.position)).filter_by(
            user_id=current_user.id, status=form.status.data
        ).scalar() or 0
        completed_at = datetime.now(timezone.utc) if form.status.data == 'done' else None
        task = Task(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            status=form.status.data,
            category_id=form.category_id.data if form.category_id.data else None,
            estimated_minutes=form.estimated_minutes.data,
            position=max_pos + 1,
            completed_at=completed_at,
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created!', 'success')
    else:
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, 'error')
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id: int):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    form.category_id.choices = _category_choices(current_user.id)
    if form.validate_on_submit():
        _set_completed_at(task, form.status.data)
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.category_id = form.category_id.data if form.category_id.data else None
        task.estimated_minutes = form.estimated_minutes.data
        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('tasks.dashboard'))
    if task.category_id:
        form.category_id.data = task.category_id
    return render_template('tasks/task_form.html', form=form, task=task)


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id: int):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Not found'}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({'success': True})


@tasks_bp.route('/tasks/reorder', methods=['PATCH'])
@login_required
def reorder_tasks():
    data = request.get_json()
    if not data or 'tasks' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    for item in data['tasks']:
        task = Task.query.filter_by(id=item['id'], user_id=current_user.id).first()
        if task:
            _set_completed_at(task, item['status'])
            task.position = item['position']
            task.status = item['status']
    db.session.commit()
    return jsonify({'success': True})


@tasks_bp.route('/tasks/<int:task_id>/timer/log', methods=['POST'])
@login_required
def log_time(task_id: int):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Not found'}), 403
    data = request.get_json()
    if not data or 'duration_seconds' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    duration = int(data['duration_seconds'])
    if duration <= 0:
        return jsonify({'error': 'Invalid duration'}), 400
    entry = TimeEntry(
        task_id=task_id,
        user_id=current_user.id,
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        duration_seconds=duration,
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({'success': True, 'total_seconds': task.total_time_seconds})


@tasks_bp.route('/categories', methods=['POST'])
@login_required
def create_category():
    name = request.form.get('name', '').strip()
    color = request.form.get('color', '#A58FE8')
    if not name or len(name) > 100:
        flash('Invalid category name.', 'error')
        return redirect(url_for('tasks.dashboard'))
    category = Category(user_id=current_user.id, name=name, color=color)
    db.session.add(category)
    db.session.commit()
    flash(f'Category "{name}" created!', 'success')
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
@login_required
def delete_category(cat_id: int):
    category = Category.query.filter_by(id=cat_id, user_id=current_user.id).first()
    if not category:
        return jsonify({'error': 'Not found'}), 403
    db.session.delete(category)
    db.session.commit()
    return jsonify({'success': True})


# ── Templates ─────────────────────────────────────────────────────────────────

@tasks_bp.route('/templates')
@login_required
def task_templates():
    templates = TaskTemplate.query.filter_by(user_id=current_user.id).order_by(
        TaskTemplate.is_default.desc(), TaskTemplate.id
    ).all()
    form = TemplateForm()
    return render_template('tasks/templates.html', templates=templates, form=form)


@tasks_bp.route('/templates', methods=['POST'])
@login_required
def create_template():
    form = TemplateForm()
    if form.validate_on_submit():
        template = TaskTemplate(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            estimated_minutes=form.estimated_minutes.data,
            emoji=form.emoji.data.strip() if form.emoji.data else '📋',
        )
        db.session.add(template)
        db.session.commit()
        flash(f'Template "{template.title}" created!', 'success')
    else:
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, 'error')
    return redirect(url_for('tasks.task_templates'))


@tasks_bp.route('/templates/<int:tmpl_id>/use', methods=['POST'])
@login_required
def use_template(tmpl_id: int):
    tmpl = TaskTemplate.query.filter_by(id=tmpl_id, user_id=current_user.id).first_or_404()
    max_pos = db.session.query(db.func.max(Task.position)).filter_by(
        user_id=current_user.id, status='todo'
    ).scalar() or 0
    task = Task(
        user_id=current_user.id,
        title=tmpl.title,
        description=tmpl.description,
        priority=tmpl.priority,
        status='todo',
        estimated_minutes=tmpl.estimated_minutes,
        position=max_pos + 1,
    )
    db.session.add(task)
    db.session.commit()
    flash(f'"{task.title}" added to To Do!', 'success')
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/templates/<int:tmpl_id>', methods=['DELETE'])
@login_required
def delete_template(tmpl_id: int):
    tmpl = TaskTemplate.query.filter_by(id=tmpl_id, user_id=current_user.id).first()
    if not tmpl:
        return jsonify({'error': 'Not found'}), 403
    db.session.delete(tmpl)
    db.session.commit()
    return jsonify({'success': True})


# ── Calendar View ──────────────────────────────────────────────────────────────

@tasks_bp.route('/calendar')
@login_required
def calendar_view():
    tasks = Task.query.filter_by(user_id=current_user.id).filter(Task.due_date.isnot(None)).all()
    priority_colors = {'low': '#00A699', 'medium': '#FC642D', 'high': '#E84393'}
    events = []
    for task in tasks:
        events.append({
            'id': task.id,
            'title': task.title,
            'start': task.due_date.isoformat(),
            'color': priority_colors.get(task.priority, '#A58FE8'),
            'url': url_for('tasks.edit_task', task_id=task.id),
            'extendedProps': {
                'priority': task.priority,
                'status': task.status,
                'description': task.description or '',
            },
        })
    return render_template('tasks/calendar.html', events=events)


# ── List View ──────────────────────────────────────────────────────────────────

@tasks_bp.route('/tasks/list')
@login_required
def task_list():
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    search = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'created_desc')

    query = Task.query.filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))

    sort_map = {
        'created_desc': Task.created_at.desc(),
        'created_asc': Task.created_at.asc(),
        'due_asc': Task.due_date.asc(),
        'due_desc': Task.due_date.desc(),
        'priority_desc': Task.priority.desc(),
        'title_asc': Task.title.asc(),
    }
    query = query.order_by(sort_map.get(sort, Task.created_at.desc()))

    tasks = query.all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    task_form = TaskForm()
    task_form.category_id.choices = _category_choices(current_user.id)

    return render_template(
        'tasks/list.html',
        tasks=tasks,
        categories=categories,
        task_form=task_form,
        today=date.today(),
        status_filter=status_filter,
        priority_filter=priority_filter,
        search=search,
        sort=sort,
    )


# ── Analytics ──────────────────────────────────────────────────────────────────

@tasks_bp.route('/analytics')
@login_required
def analytics():
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    today = date.today()

    status_counts = {'todo': 0, 'in_progress': 0, 'done': 0}
    for t in all_tasks:
        status_counts[t.status] = status_counts.get(t.status, 0) + 1

    priority_counts = {'low': 0, 'medium': 0, 'high': 0}
    for t in all_tasks:
        priority_counts[t.priority] = priority_counts.get(t.priority, 0) + 1

    daily_labels = []
    daily_created = []
    daily_completed = []
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        daily_labels.append(d.strftime('%b %d'))
        created_count = sum(
            1 for t in all_tasks
            if t.created_at and t.created_at.date() == d
        )
        completed_count = sum(
            1 for t in all_tasks
            if t.completed_at and t.completed_at.date() == d
        )
        daily_created.append(created_count)
        daily_completed.append(completed_count)

    categories = Category.query.filter_by(user_id=current_user.id).all()
    cat_labels = [c.name for c in categories]
    cat_counts = [sum(1 for t in all_tasks if t.category_id == c.id) for c in categories]
    cat_colors = [c.color for c in categories]
    uncategorized = sum(1 for t in all_tasks if t.category_id is None)
    if uncategorized:
        cat_labels.append('Uncategorized')
        cat_counts.append(uncategorized)
        cat_colors.append('#C9B8F5')

    overdue_count = sum(
        1 for t in all_tasks
        if t.due_date and t.due_date < today and t.status != 'done'
    )

    all_entries = TimeEntry.query.filter_by(user_id=current_user.id).all()
    total_seconds = sum(e.duration_seconds for e in all_entries if e.duration_seconds)
    total_hours = round(total_seconds / 3600, 1)

    completion_rate = round((status_counts['done'] / len(all_tasks) * 100) if all_tasks else 0, 1)

    avg_completion_days = None
    completed_with_time = [
        t for t in all_tasks
        if t.status == 'done' and t.completed_at and t.created_at
    ]
    if completed_with_time:
        total_days = sum(
            (t.completed_at.replace(tzinfo=timezone.utc) - t.created_at.replace(tzinfo=timezone.utc)).days
            for t in completed_with_time
        )
        avg_completion_days = round(total_days / len(completed_with_time), 1)

    return render_template(
        'tasks/analytics.html',
        status_counts=status_counts,
        priority_counts=priority_counts,
        daily_labels=daily_labels,
        daily_created=daily_created,
        daily_completed=daily_completed,
        cat_labels=cat_labels,
        cat_counts=cat_counts,
        cat_colors=cat_colors,
        overdue_count=overdue_count,
        total_hours=total_hours,
        completion_rate=completion_rate,
        total_tasks=len(all_tasks),
        avg_completion_days=avg_completion_days,
    )
