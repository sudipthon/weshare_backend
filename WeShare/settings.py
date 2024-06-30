# import environ
import dj_database_url
import os
from pathlib import Path

DJANGO_SETTINGS_MODULE = "WeShare.settings"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-a+r-!&#7bc_7hbg!hg_-b)0&!b)*&x18@iqlg9^cru*!mb8$qa"
AUTH_USER_MODEL = "Account.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "Account.backend.EmailBackend",
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://192.168.1.73:8000",
#     "https://weshare-mo9u.onrender.com",
#     "http://localhost:5173"
# ]  # if

# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Account.apps.AccountConfig",
    # packages
    "django_extensions",
    # "django.contrib.sites",
    # rest related apps
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    # custom apps
    "Posts",
    "Message",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "WeShare.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "WeShare.wsgi.application"
ASGI_APPLICATION = "WeShare.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


EXTERNAL_DATABASE_URL = "postgresql://sudip:SpZm4WJXZGuzihVOD7eA6VK6nFoRSUwv@dpg-cq00fk6ehbks73e4ihc0-a.oregon-postgres.render.com/weshare_ger0"
INTERNAL_DATABASE_URL = "postgresql://sudip:SpZm4WJXZGuzihVOD7eA6VK6nFoRSUwv@dpg-cq00fk6ehbks73e4ihc0-a/weshare_ger0"
# INTERNAL_DATABASE_URL= os.environ.get("INTERNAL_DATABASE_URL")
DATABASES = {
    "default": dj_database_url.config(
        default=EXTERNAL_DATABASE_URL,
        conn_max_age=600,
    )
}

# DATABASES = {

#     "default": {q

#         "ENGINE": "django.db.backends.postgresql",
#         "host": "dpg-cq00fk6ehbks73e4ihc0-a",
#         "name": "weshare",
#         "user": "sudip",
#         "password": "SpZm4WJXZGuzihVOD7eA6VK6nFoRSUwv",
#         "port": 5432,
#         "conn_max_age": 600,
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",  # Add this
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 6,
}


# STATIC_URL = "/home/myusername/myproject/static/"
# STATICFILES_DIRS = [
#     BASE_DIR / "statics",
# ]
# STATIC_ROOT="/home/myusername/myproject/staticfiles/"
# MEDIA_URL = "/media/"
# # Default primary key field type
# # https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


redis_host = "redis-16026.c81.us-east-1-2.ec2.redns.redis-cloud.com"
redis_port = 16026
redis_password = "p6J3UvtNJ43sfyvdgfEG2FdMjLuyVJfV"

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://:{redis_password}@{redis_host}:{redis_port}"],
        },
    },
}
# env = environ.Env(
#     DEBUG=(bool, False)

# )
# environ.Env.read_env()  # reads the .env file


# SITE_ID = 1

# import redis


# redis_host = 'redis-16026.c81.us-east-1-2.ec2.redns.redis-cloud.com'
# redis_port = 16026
# redis_password = 'p6J3UvtNJ43sfyvdgfEG2FdMjLuyVJfV'

# client = redis.StrictRedis(
#     host=redis_host,
#     port=redis_port,
#     password=redis_password,
#     decode_responses=True
# )

# try:
#     response = client.ping()
#     if response:
#         print("Connected to Redis")
# except redis.ConnectionError:
#     print("Failed to connect to Redis")
