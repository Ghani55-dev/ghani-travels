from pathlib import Path
import os
import openai

from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x7nj1fz%z_a-04@bkyq!^0x@zl4%+fn2ze^v-h4hcgso9!1=h@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'sslserver',
    'django_extensions',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS': [BASE_DIR / 'templates'], 
        'DIRS': [BASE_DIR / "myapp/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database Configuration (Using SQLite or PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'myapp', 'static')]  # Static files directory

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Media files directory

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security Settings (in development set to False)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
# CSRF_USE_SESSIONS = True
# CORS configuration (if needed)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


# Custom error handlers (optional)
handler404 = 'myapp.views.handler404' 
handler500 = 'myapp.views.handler500'

# Authentication backends (optional)
AUTHENTICATION_BACKENDS = [
    #'myapp.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Logging configuration (optional)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'filename': 'payment_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


# Stripe Test Keys (optional)
STRIPE_TEST_PUBLIC_KEY = 'pk_test_51R7KP9P6E8Ea1jTc1WvcBRxwbu7pEXqObeDlZVY6761a67ysh4J2A4WSvzduarAiPL7WooUpapgE7ybDM482v7mK00iXPHL3aF'
STRIPE_TEST_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_TEST_WEBHOOK_SECRET = ' whsec_f914a26f0083d8ad771866fecd9bf62057ed52e1b4de83d26e6c62f3630b6bd4'
DEFAULT_FROM_EMAIL = 'ganaganiganesh5268@gmail.com'


UPI_ID = '8978941066@ybl'
MERCHANT_NAME = 'Ghani Travels'

TICKET_PRICES = {
    'general': 500,
    'vip': 1000,
    'premium': 1500
}

# OpenAI API Key (optional)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

APPEND_SLASH = False

LOGIN_URL = '/login/'

# Custom User Model (if using)
# AUTH_USER_MODELS = 'myapp.CustomUser'
AUTH_USER_MODEL = 'myapp.CustomUser'

# AUTH_USER_MODEL  = 'myapp.CustomUser'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

LOGOUT_REDIRECT_URL = "/login/"
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Ensure these session settings are configured
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # Or 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 3600  # 1 hour session timeout
SESSION_COOKIE_SECURE = True  # For production (HTTPS)
# SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = True  # Helps keep session alive

# Email Configuration

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'ganaganiganesh5268@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # e.g., smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ganamunna143@gmail.com'
EMAIL_HOST_PASSWORD = 'yhvz sfyj zzkl lzav'