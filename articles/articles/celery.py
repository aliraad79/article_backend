from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "articles.settings")

app = Celery("articles")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "fetch-and-store-temp-data-contrab": {
        "task": "main.tasks.make_votes_valid",
        "schedule": crontab(minute="*/15"),
    }
}
