# to import celery app as soon as django server starts

from .celery import app as celery_app

__all__ = ('celery_app',)
