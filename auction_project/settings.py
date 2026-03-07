from pathlib import Path
import os

# ================================
# BASE DIRECTORY
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ================================
# SECURITY SETTINGS
# ================================
SECRET_KEY = 'django-insecure-m+q9)g8wlok(1o46)qi2yi1j%xg-gm*g9q$3$-4--vii$cbq!2'

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "elitecricket.co.in",
    "www.elitecricket.co.in",
    "elite-cricket-auction.onrender.com"
]


# ================================
# APPLICATIONS
# ================================
INSTALLED_APPS = [
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',   # ✅ Add this

    # Our Auction App
    'players',
]
# ================================
# MIDDLEWARE
# ================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'players.middleware.MaintenanceMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ================================
# URL CONFIG
# ================================
ROOT_URLCONF = 'auction_project.urls'


# ================================
# TEMPLATES
# ================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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


# ================================
# WSGI
# ================================
WSGI_APPLICATION = 'auction_project.wsgi.application'


# ================================
# DATABASE
# ================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ================================
# PASSWORD VALIDATION
# ================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ================================
# INTERNATIONALIZATION
# ================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True
USE_TZ = True


# ================================
# STATIC FILES
# ================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# ================================
# MEDIA FILES
# ================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ================================
# DEFAULT FIELD
# ================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ================================
# RAZORPAY CONFIGURATION
# ================================
RAZORPAY_KEY_ID = "rzp_live_SNVYf99QxHGWX0"
RAZORPAY_KEY_SECRET = "6rEzvzXnnrlvyftKpndNvtVA"


# ================================
# AUCTION CONTROL
# ================================
AUCTION_ENABLED = False


# ================================
# EMAIL SETTINGS
# ================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "sauravrathore25102002@gmail.com"
EMAIL_HOST_PASSWORD = "hkauftdymjnmtrvv"

DEFAULT_FROM_EMAIL = "Elite Cricket Auction <yourgmail@gmail.com>"
ADMIN_EMAIL = "ar783524@gmail.com"