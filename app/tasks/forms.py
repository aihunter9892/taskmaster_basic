from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=2000)])
    due_date = DateField('Due Date', validators=[Optional()])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    status = SelectField('Status', choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')], default='todo')
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    estimated_minutes = IntegerField('Estimated (min)', validators=[Optional(), NumberRange(min=1, max=9999)])
    submit = SubmitField('Save Task')


class TemplateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=2000)])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    estimated_minutes = IntegerField('Estimated (min)', validators=[Optional(), NumberRange(min=1, max=9999)])
    emoji = StringField('Emoji', validators=[Optional(), Length(max=10)])
    submit = SubmitField('Save Template')
