import os

from django.conf import settings

from celery import Celery
from celery.signals import setup_logging  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shipping.settings")

app = Celery(
    "shipping",
    include=[
        "shipping_service.shipping.cron",
    ],
)


app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.broker_transport_options = {
    "visibility_timeout": 3600,
    "max_retries": 1,
    "broker_connection_timeout": 30.0,
}


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa

    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)


app.autodiscover_tasks()


app.conf.beat_schedule = {}
