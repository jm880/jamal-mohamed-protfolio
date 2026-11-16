import os
from pathlib import Path
from urllib.parse import urlparse
BASE_DIR = Path(__file__).resolve().parent.parent
def env_bool(key, default=False): return os.getenv(key, str(default)).lower() in ("1", "true", "yes")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = [x.strip() for x in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if x.strip()]
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "portfolio"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR / "templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
_database_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
if _database_url.startswith("sqlite:///"):
    DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR / _database_url.removeprefix("sqlite:///")}}
elif _database_url.startswith("postgres"):
    p=urlparse(_database_url); DATABASES={"default":{"ENGINE":"django.db.backends.postgresql","NAME":p.path.lstrip("/"),"USER":p.username,"PASSWORD":p.password,"HOST":p.hostname,"PORT":p.port or 5432,"CONN_MAX_AGE":60,"OPTIONS":{"sslmode":"require" if not DEBUG else "prefer"}}}
else: raise RuntimeError("DATABASE_URL must be a sqlite or postgres URL")
AUTH_PASSWORD_VALIDATORS = [{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE="en-us"
TIME_ZONE="Africa/Cairo"
USE_I18N=True
USE_TZ=True
STATIC_URL="static/"
STATIC_ROOT=BASE_DIR / "staticfiles"
STATICFILES_DIRS=[BASE_DIR / "static"]
MEDIA_URL="/media/"
MEDIA_ROOT=BASE_DIR / "media"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
LOGIN_URL="/admin/login/"
EMAIL_BACKEND=os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL=os.getenv("DEFAULT_FROM_EMAIL", "portfolio@localhost")
CONTACT_NOTIFY_EMAIL=os.getenv("CONTACT_NOTIFY_EMAIL", "")
FILE_UPLOAD_MAX_MEMORY_SIZE=5*1024*1024
DATA_UPLOAD_MAX_MEMORY_SIZE=5*1024*1024
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS="DENY"
CSRF_COOKIE_SECURE=not DEBUG
SESSION_COOKIE_SECURE=not DEBUG
SECURE_SSL_REDIRECT=not DEBUG
SECURE_HSTS_SECONDS=31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS=not DEBUG
SECURE_HSTS_PRELOAD=not DEBUG
