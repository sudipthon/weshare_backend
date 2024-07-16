

import os

from django.core.wsgi import get_wsgi_application
import os
import sys

from dotenv import load_dotenv

load_dotenv()
DJANGO_ENV = os.environ.get("DJANGO_ENV")


if DJANGO_ENV == "server":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeShare.server_settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeShare.local_settings")

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeShare.local_settings')

application = get_wsgi_application()
