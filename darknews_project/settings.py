"""
Django settings for darknews_project project.
"""

from pathlib import Path
import os

# -------------------------
# BASE DIR
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# SECURITY
# -------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "9#16o&evme2rc&*6vd3xd^o!rpu#-w_r1j%yd#z9-@ggq8k3ga"
)
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = ["*"]  # Change to your domain in production

# -------------------------
# APPLICATIONS
# -------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
    'final',
    'django.contrib.humanize',
]

# -------------------------
# MIDDLEWARE
# -------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # must be after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------
# URLS AND TEMPLATES
# -------------------------
ROOT_URLCONF = 'darknews_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # explicit templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'darknews_project.wsgi.application'

# -------------------------
# DATABASE
# -------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------
# PASSWORD VALIDATION
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# -------------------------
# INTERNATIONALIZATION
# -------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------
# STATIC FILES
# -------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # local static folder
STATIC_ROOT = BASE_DIR / 'staticfiles'    # collectstatic destination
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------
# MEDIA / CLOUDINARY
# -------------------------
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME", "dai4fmwr2"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY", "513374976163413"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET", "383225161215924"),
}

# -------------------------
# LOGIN / LOGOUT
# -------------------------
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"
LOGIN_URL = "/login/"

# -------------------------
# DEFAULT AUTO FIELD
# -------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
