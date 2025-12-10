from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'assets') ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True      # TLS ON
EMAIL_USE_SSL = False     # SSL must be OFF

EMAIL_HOST_USER = 'alifelectronics365@gmail.com'
EMAIL_HOST_PASSWORD = 'neaf fmif zpcj kzvw'   # NOT your Gmail login password

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# neaf fmif zpcj kzvw