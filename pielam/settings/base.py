import os
from pathlib import Path

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Adjust accordingly


SECRET_KEY = os.environ.get("'django-insecure-o@6wohmtl^b*nyy90+mz92_yywtm(ik6ykikzxt%q)(&l-4t4y'", "dev-secret-key")

DEBUG = False

INSTALLED_APPS = [
    # Django default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Installed Apps
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',

    # My Appa
    "apps.ponno",
    "apps.customer",
    "apps.kobutor",
    "apps.core",
    "apps.tomal",
    "apps.notify",
   
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pielam.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
         'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Optional if you want a global templates folder
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "pielam.wsgi.application"
ASGI_APPLICATION = "pielam.asgi.application"



AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'customer.User'

