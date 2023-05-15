"""
WSGI config for spm_pj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from apscheduler.schedulers.background import BackgroundScheduler

from main.tasks.reservation_task import check_reservations

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spm_pj.settings")

application = get_wsgi_application()

scheduler = BackgroundScheduler()
scheduler.add_job(check_reservations, 'interval', seconds=10)
scheduler.start()