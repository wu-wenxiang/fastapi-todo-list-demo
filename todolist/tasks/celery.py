from celery import Celery

app = Celery()
app.config_from_object("todolist.tasks.celeryconfig")
# app.autodiscover_tasks(['todolist.tasks'], related_name="schedules")
