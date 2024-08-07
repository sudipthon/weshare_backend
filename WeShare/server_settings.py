import os
from .settings import *
import dj_database_url

from dotenv import load_dotenv
load_dotenv()
DEBUG = True
DJANGO_ENV = os.environ.get("DJANGO_ENV")

DATABASE_URL = os.environ.get("DATABASE_URL")
# DATABASES = {
#     "default": dj_database_url.config(
#         default=DATABASE_URL,
#         conn_max_age=600,
#     )
# }


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"],
        },
    },
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


