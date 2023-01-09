from celery import Celery

app = Celery("celery_tasks")
app.config_from_object("celery_tasks.celery_config")

