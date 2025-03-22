"""
Django settings for mealplanner project.
"""

import os
from pathlib import Path

from everett.manager import ListOf

from base.config_manager import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEALPLANNER_PROJECT_DIR = Path(__file__).resolve().parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", parser=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", parser=bool, default="False")

# The `allow_empty=True` ensures the split operation works even when nothing follows the comma
# We then use `filter()` to remove any resulting empty strings from the list
ALLOWED_HOSTS = list(
    filter(
        None,
        config(
            "ALLOWED_HOSTS",
            parser=ListOf(
                str,
                allow_empty=True,
            ),
            default="localhost"
        )
    )
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chef",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mealplanner.urls"

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

WSGI_APPLICATION = "mealplanner.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = MEALPLANNER_PROJECT_DIR / "static_collected"
STATICFILES_DIRS = [
    BASE_DIR / "chef" / "static",
]
# same as:
# STATIC_ROOT = BASE_DIR / "mealplanner" / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django registration

ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window

# For now, after signing in, go to the root page, which is the meal schedule
LOGIN_REDIRECT_URL = "/"

# Email setup

_email_host = config("EMAIL_HOST", parser=str, default="")
_email_host_password = config("EMAIL_HOST_PASSWORD", parser=str, default="")
_email_host_user = config("EMAIL_HOST_USER", parser=str, default="")

if ( _email_host and _email_host_password and _email_host_user):
    print("Using SMTP email")
    EMAIL_HOST = _email_host
    EMAIL_HOST_PASSWORD = _email_host_password
    EMAIL_HOST_USER = _email_host_user
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
else:
    print("Warning! Using console backend for email!")
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
