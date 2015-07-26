import datetime

from peewee import *

DATABASE = SqliteDatabase('projects.db')

class Project(Model):
    name = CharField(unique = True)
    description = TextField()
    date_created = DateTimeField(default=datetime.datetime.now)
    url = CharField(unique = True)

    class Meta:
        database = DATABASE
        order_by = ('name',)

    def remaining(self):
        return Task.select().where(Task.project==self,Task.completed==False).count()

    def completed(self):
        return Task.select().where(Task.project==self,Task.completed==True).count()

    @classmethod
    def create_project(cls,name, description):
        try:
            with DATABASE.transaction():
                cls.create(
                    name = name,
                    description = description,
                    url = name.replace(" ","_")
                )
        except IntegrityError:
            raise ValueError("Project already exists")

class Task(Model):
    title = CharField(unique = True)
    details = TextField()
    date_created = DateTimeField(default=datetime.datetime.now)
    lastdate = DateTimeField(default=datetime.datetime.now)
    completed = BooleanField(default=False)
    url = CharField(unique=True)
    project = ForeignKeyField(
        rel_model=Project,
        related_name='task'
    )

    class Meta:
        database = DATABASE
        order_by = ('date_created',)

    @classmethod
    def create_task(cls, title, details, lastdate, project,completed = False):
        try:
            with DATABASE.transaction():
                cls.create(
                    title = title,
                    details = details,
                    lastdate = lastdate,
                    completed = completed,
                    url = title.replace(" ","_"),
                    project = project
                )
        except ValueError:
            print("Task already exists")

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Project, Task], safe = True)
