import os
from .settings import *
import dj_database_url

from dotenv import load_dotenv
load_dotenv()
DEBUG = True

INTERNAL_DATABASE_URL = os.environ.get("INTERNAL_DATABASE_URL")
DATABASES = {
    "default": dj_database_url.config(
        default=INTERNAL_DATABASE_URL,
        conn_max_age=600,
    )
}

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
