"""
Django settings for darknews_project project (Render-ready, production safe)
"""

from pathlib import Path
import os

# -------------------------------------------------
# BASE DIR
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------
# SECURITY
# -------------------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "9#16o&evme2rc&*6vd3xd^o!rpu#-w_r1j%yd#z9-@ggq8k3ga"
)

# DEBUG should always be False in production
DEBUG = os.environ.get("DEBUG", "False") == "True"


ALLOWED_HOSTS = [
    "caseboard.online",
    "www.caseboard.online",
    "detective-webapp.onrender.com",
    ".onrender.com",
    "localhost",
    "127.0.0.1",
]


CSRF_TRUSTED_ORIGINS = [
    "http://caseboard.online",
    "http://www.caseboard.online",
    "https://caseboard.online",
    "https://www.caseboard.online",
    "https://detective-webapp.onrender.com",
]



# -------------------------------------------------
# APPLICATIONS
# -------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "cloudinary",
    "cloudinary_storage",

    "final",  # your main app

    "django.contrib.humanize",
]

# -------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------------------------
# URLS / WSGI
# -------------------------------------------------
ROOT_URLCONF = "darknews_project.urls"
WSGI_APPLICATION = "darknews_project.wsgi.application"

# -------------------------------------------------
# TEMPLATES
# -------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # app templates are enough
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

# -------------------------------------------------
# DATABASE
# -------------------------------------------------
# Default: SQLite (good for Render, simple apps)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Optional: Postgres on Render (uncomment if using Postgres)
# import dj_database_url
# DATABASES = {
#     "default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))
# }

# -------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# STATIC FILES (CSS / JS)
# -------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Use WhiteNoise to serve static files on Render
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------------------------------------
# MEDIA FILES (CLOUDINARY)
# -------------------------------------------------
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
# Make sure you set CLOUDINARY_URL in Render Environment
# Format: cloudinary://API_KEY:API_SECRET@CLOUD_NAME

# -------------------------------------------------
# AUTH REDIRECTS
# -------------------------------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

# -------------------------------------------------
# DEFAULT PRIMARY KEY
# -------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

