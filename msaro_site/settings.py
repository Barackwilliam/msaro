"""
Django settings for the Msaro Guide Tanzania website.

Everything that differs between your computer and the live server comes from
environment variables (see .env.example):

* DATABASE_URL        Supabase Postgres connection string. Without it a local
                      SQLite file is used, which is handy for development.
* SUPABASE_S3_*       Supabase Storage (S3-compatible) keys + bucket. Without
                      them uploaded images are saved in ./media on the disk.
"""
import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def env(name, default=None):
    value = os.environ.get(name)
    return value if value not in (None, "") else default


def env_bool(name, default=False):
    return str(env(name, default)).strip().lower() in ("1", "true", "yes", "on")


# Optional .env file for local development (never commit the real one).
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _value = _line.split("=", 1)
            os.environ.setdefault(_key.strip(), _value.strip().strip('"').strip("'"))


SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = env_bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = [h.strip() for h in env(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,.onrender.com,msaroguidetanzania.com,www.msaroguidetanzania.com",
).split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in env(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "https://*.onrender.com,https://msaroguidetanzania.com,https://www.msaroguidetanzania.com",
).split(",") if o.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "website",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "msaro_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "website.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "msaro_site.wsgi.application"


# --- Database: Supabase Postgres -------------------------------------------
# Use the "Session pooler" connection string from Supabase
# (Project Settings -> Database -> Connection string), e.g.
# postgresql://postgres.<ref>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=env_bool("DATABASE_SSL_REQUIRE", str(env("DATABASE_URL", "")).startswith("postgres")),
    )
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Static files (CSS/JS) via WhiteNoise -------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
# Files in ./public are served from the site root, so old links such as
# /images/og-cover.jpg, /robots.txt and /sitemap.xml keep working.
WHITENOISE_ROOT = BASE_DIR / "public"
# Serve straight from ./static too, so the site still has its CSS even if a
# deploy ever skipped collectstatic.
WHITENOISE_USE_FINDERS = True


# --- Uploaded images: Supabase Storage bucket ---------------------------------
# Supabase -> Storage -> Settings -> "S3 Connection": copy the endpoint and
# region, and create an access key. The bucket must be set to *public*.
SUPABASE_S3_ENDPOINT = env("SUPABASE_S3_ENDPOINT")          # https://<ref>.supabase.co/storage/v1/s3
SUPABASE_S3_REGION = env("SUPABASE_S3_REGION", "us-east-1")
SUPABASE_S3_ACCESS_KEY_ID = env("SUPABASE_S3_ACCESS_KEY_ID")
SUPABASE_S3_SECRET_ACCESS_KEY = env("SUPABASE_S3_SECRET_ACCESS_KEY")
SUPABASE_STORAGE_BUCKET = env("SUPABASE_STORAGE_BUCKET", "media")
SUPABASE_PROJECT_URL = env("SUPABASE_PROJECT_URL")          # https://<ref>.supabase.co

USE_SUPABASE_STORAGE = bool(SUPABASE_S3_ENDPOINT and SUPABASE_S3_ACCESS_KEY_ID and SUPABASE_S3_SECRET_ACCESS_KEY)

if USE_SUPABASE_STORAGE:
    if SUPABASE_PROJECT_URL:
        _public_host = SUPABASE_PROJECT_URL.replace("https://", "").replace("http://", "").rstrip("/")
    else:
        _public_host = SUPABASE_S3_ENDPOINT.replace("https://", "").split("/storage/")[0]
    default_storage = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "endpoint_url": SUPABASE_S3_ENDPOINT,
            "region_name": SUPABASE_S3_REGION,
            "access_key": SUPABASE_S3_ACCESS_KEY_ID,
            "secret_key": SUPABASE_S3_SECRET_ACCESS_KEY,
            "bucket_name": SUPABASE_STORAGE_BUCKET,
            # Public bucket: plain, permanent URLs (no expiring signatures).
            "custom_domain": f"{_public_host}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}",
            "querystring_auth": False,
            "file_overwrite": False,
            "default_acl": None,
            "addressing_style": "path",
            "signature_version": "s3v4",
            "object_parameters": {"CacheControl": "public, max-age=31536000"},
        },
    }
    MEDIA_URL = f"https://{_public_host}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/"
else:
    default_storage = {"BACKEND": "django.core.files.storage.FileSystemStorage"}
    MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": default_storage,
    "staticfiles": {"BACKEND": "website.storage.StaticStorage"},
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024


# --- Security for the live site ----------------------------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Dar_es_Salaam"
USE_I18N = True
USE_TZ = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
