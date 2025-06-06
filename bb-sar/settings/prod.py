from .base import *

DEBUG = True
ALLOWED_HOSTS = ['bb-sar.onrender.com']

# Where static files are collected by collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add this to avoid errors with static collection
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Recommended: Don't hardcode SECRET_KEY
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fallback-insecure-key")
