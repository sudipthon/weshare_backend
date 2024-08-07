#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv


load_dotenv()
DJANGO_ENV = os.environ.get("DJANGO_ENV")


def main():
    """Run administrative tasks."""
    if DJANGO_ENV == "server":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeShare.server_settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeShare.local_settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()



