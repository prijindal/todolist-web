from flask_wtf import Form
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import (DataRequired, ValidationError)

from models import Project, Task

def project_exists(form, field):
    if Project.select().where(Project.name == field.data).exists():
        raise ValidationError("Project with that name already exists")

def task_exists(form, field):
    if Task.select().where(Task.title == field.data).exists():
        raise ValidationError("Task with that name already exists")

class ProjectForm(Form):
    name = StringField(
        'Project Name',
        validators = [
            DataRequired(),
            project_exists
        ]
    )
    description = TextAreaField(
        'Description'
    )

class TaskForm(Form):
    title = StringField(
        'Task Name',
        validators = [
            DataRequired(),
            task_exists
        ]
    )
    details = TextAreaField(
        'Describe Task'
    )
    lastdate = DateField(
        'Enter Last Date',
        validators = [DataRequired()]
    )
