"""
Django settings for guidenetwork project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

try:
    from .keys import secret_key, db_password
except ImportError as e:
    print(
        "\n***********************************\n\nWARNING: {}. Using default configuration. This should ONLY be used by Travis for build testing.\n\n***********************************\n".format(
            e
        )
    )
    db_password = ""
    secret_key = "3u57j-w!+4m_k-f1(or!1d_n4bmrwi!+a@x9xvdt^r0qs(jj@!"  # NOTE: This is an alternate secret key for build testing ONLY!

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "172.19.87.88"]


# Application definition

INSTALLED_APPS = [
    "home.apps.HomeConfig",
    "accounts.apps.AccountsConfig",
    "transactions.apps.TransactionsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users.apps.UsersConfig",
    "crispy_forms",
    "ajax_select",
]
CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sterling.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR + "/sterling/templates"],
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

WSGI_APPLICATION = "sterling.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sterling",
        "USER": "postgres",
        "PASSWORD": db_password,
        "HOST": "172.19.80.1",
        "PORT": "5432",
    }
    # "default": {
    #     "ENGINE": "mysql.connector.django",
    #     "NAME": "sterling",
    #     "USER": "root",
    #     "PASSWORD": db_password,
    #     "HOST": "localhost",
    #     "PORT": "3306",
    #     "OPTIONS": {"autocommit": True},
    # }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AJAX_LOOKUP_CHANNELS = {
    # specify a lookup to be loaded
    # str: tuple
    "categories": ("transactions.lookups", "CategoryLookup"),
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "sterling/media")

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "login"

LOGOUT_URL = "logout"


LOGIN_REDIRECT_URL = "users:login_redirect"

LOGOUT_REDIRECT_URL = "home:home"
