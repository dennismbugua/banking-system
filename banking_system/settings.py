"""
Django Settings for Banking System

This configuration is optimized for production deployment on Vercel with Supabase PostgreSQL,
while maintaining compatibility for local development. The settings automatically detect
the environment and adjust accordingly.
"""

from django.core.management.utils import get_random_secret_key
from pathlib import Path
import os

# Load environment variables from .env file
# WHY: Keeps sensitive data like secret keys and database credentials out of version control
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# WHY: Using Path object provides cross-platform compatibility and cleaner path operations
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# WHY: Secret key is used for cryptographic signing. Environment variable allows different keys for dev/prod
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())


# Environment Detection
# WHY: Automatically detect if running in production or development
IS_PRODUCTION = os.getenv('VERCEL_ENV') == 'production' or os.getenv('DJANGO_ENV') == 'production'
IS_LOCAL = not IS_PRODUCTION and (
    '127.0.0.1' in os.getenv('DJANGO_ALLOWED_HOSTS', '') or 
    'localhost' in os.getenv('DJANGO_ALLOWED_HOSTS', '') or
    not os.getenv('DJANGO_ALLOWED_HOSTS')
)


# DEBUG Configuration
# WHY: Debug mode shows detailed error pages with sensitive information that shouldn't be exposed in production
# PRODUCTION: False for security
# LOCAL: True for detailed error messages
DEBUG = IS_LOCAL or os.getenv("DEBUG", "False").lower() == "true"


# Allowed Hosts Configuration
# WHY: Defines which hosts/domains are allowed to serve this Django application
if IS_PRODUCTION:
    # PRODUCTION: Secure host configuration
    ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", ".vercel.app").split(",")
else:
    # LOCAL DEVELOPMENT: Allow localhost and common development hosts
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0', '.ngrok.io', '.herokuapp.com'] + \
                   os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if os.getenv("DJANGO_ALLOWED_HOSTS") else ['127.0.0.1', 'localhost', '0.0.0.0']


# Application definition
# WHY: These are all the Django apps that make up your banking system
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',           # Admin interface
    'django.contrib.auth',            # Authentication system
    'django.contrib.contenttypes',    # Content type framework
    'django.contrib.sessions',        # Session framework
    'django.contrib.messages',        # Messaging framework
    'django.contrib.staticfiles',     # Static files management

    # Third-party apps
    'django_celery_beat',             # Celery periodic task scheduler

    # Local apps
    'accounts',                       # User account management
    'core',                          # Core banking functionality
    'transactions',                   # Financial transactions
]


# Middleware Configuration
# WHY: Middleware components are processed in order for each request/response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Security enhancements
    'whitenoise.middleware.WhiteNoiseMiddleware',         # Static files serving for production
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',          # Common operations
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Message framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]


# URL Configuration
# WHY: Defines the main URL configuration module
ROOT_URLCONF = 'banking_system.urls'

# Custom User Model
# WHY: Specifies custom user model instead of Django's default User model
# This allows for banking-specific user fields and functionality
AUTH_USER_MODEL = 'accounts.User'


# Template configuration
# WHY: Defines how Django finds and renders HTML templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Custom template directory
        'APP_DIRS': True,  # Look for templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',     # Debug info in templates
                'django.template.context_processors.request',   # Request object in templates
                'django.contrib.auth.context_processors.auth',  # User info in templates
                'django.contrib.messages.context_processors.messages',  # Messages in templates
            ],
        },
    },
]


# WSGI Application
# WHY: Points to the WSGI application for deployment
if IS_PRODUCTION:
    # PRODUCTION: Vercel-compatible WSGI application
    WSGI_APPLICATION = 'banking_system.wsgi.app'
else:
    # LOCAL DEVELOPMENT: Standard Django WSGI application
    WSGI_APPLICATION = 'banking_system.wsgi.application'


# Database Configuration
# WHY: Database settings determine where your data is stored and how to connect
if IS_PRODUCTION or os.getenv("USE_POSTGRES", "False").lower() == "true":
    # PRODUCTION: Supabase PostgreSQL database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("DB_NAME", "postgres"),
            'USER': os.getenv("DB_USER"),
            'PASSWORD': os.getenv("DB_PASSWORD"),
            'HOST': os.getenv("DB_HOST"),
            'PORT': os.getenv("DB_PORT", "5432"),
            'OPTIONS': {
                'sslmode': 'require',  # Required for Supabase connections
                'connect_timeout': 60,
                'options': '-c default_transaction_isolation=serializable'
            },
            'CONN_MAX_AGE': 600,  # Connection pooling
        }
    }
else:
    # LOCAL DEVELOPMENT: SQLite database (fallback for local development)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# WHY: Ensures users create secure passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # Prevents passwords too similar to user information
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},  # Minimum 8 characters for security
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # Prevents common passwords like "password123"
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Prevents entirely numeric passwords
    },
]


# Internationalization
# WHY: Configures language, timezone, and localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'  # Set to Kenya timezone for banking operations
USE_I18N = True   # Enable internationalization
USE_L10N = True   # Enable localization
USE_TZ = True     # Enable timezone support


# Static Files Configuration
# WHY: Configures how static assets are served and collected
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where collectstatic puts files

if not IS_PRODUCTION:
    # LOCAL DEVELOPMENT: Additional static files directories
    STATICFILES_DIRS = [BASE_DIR / 'static']

# Static files storage for production
# WHY: Optimizes static file serving for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# WhiteNoise configuration for production static files
# WHY: Efficiently serves static files in production without a separate server
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = not IS_PRODUCTION


# Banking System Specific Settings
# WHY: Business logic configuration for the banking application
ACCOUNT_NUMBER_START_FROM = 1000000000  # Starting account number for new accounts
MINIMUM_DEPOSIT_AMOUNT = 100           # Minimum KES amount for deposits
MINIMUM_WITHDRAWAL_AMOUNT = 100        # Minimum KES amount for withdrawals


# Authentication Settings
# WHY: Defines where users go after successful login
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'


# Session Configuration
# WHY: Configures user session behavior
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# Celery Configuration (Task Queue)
# WHY: Handles background tasks like sending emails, processing transactions
if IS_PRODUCTION:
    # PRODUCTION: Redis-based task queue
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379')
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE
    CELERY_TASK_ALWAYS_EAGER = False
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
else:
    # LOCAL DEVELOPMENT: Run tasks synchronously (no Redis required)
    CELERY_TASK_ALWAYS_EAGER = True        # Execute tasks immediately
    CELERY_TASK_EAGER_PROPAGATES = True    # Propagate exceptions immediately


# Model Configuration
# WHY: Defines default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Security Settings
# WHY: Enhanced security measures for production deployment
if IS_PRODUCTION:
    # PRODUCTION: Full security configuration
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_SSL_REDIRECT = True
    X_FRAME_OPTIONS = 'DENY'
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Strict'
    SESSION_COOKIE_SAMESITE = 'Strict'
else:
    # LOCAL DEVELOPMENT: Relaxed security for development
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False


# Cache Configuration
# WHY: Improves performance through caching
if IS_PRODUCTION and os.getenv('REDIS_URL'):
    # PRODUCTION: Redis cache
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.getenv('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    # LOCAL DEVELOPMENT: Database cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'banking_cache_table',
        }
    }


# Logging Configuration
# WHY: Helps with debugging and monitoring
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple' if IS_LOCAL else 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        } if IS_PRODUCTION else {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'] if IS_PRODUCTION else ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'] if IS_PRODUCTION else ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'banking_system': {
            'handlers': ['console', 'file'] if IS_PRODUCTION else ['console'],
            'level': 'DEBUG' if IS_LOCAL else 'INFO',
            'propagate': False,
        },
    },
}


# Email Configuration
# WHY: Required for sending emails from the banking system
if IS_PRODUCTION:
    # PRODUCTION: SMTP email backend
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@yourbank.com')
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
else:
    # LOCAL DEVELOPMENT: Console email backend for testing
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# File Upload Settings
# WHY: Security settings for file uploads
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000


# Environment-specific configurations
if IS_PRODUCTION:
    # Create logs directory if it doesn't exist
    os.makedirs(BASE_DIR / 'logs', exist_ok=True)
    
    # Additional production-only settings
    ADMINS = [
        ('Admin', os.getenv('ADMIN_EMAIL', 'banking@online.com')),
    ]
    MANAGERS = ADMINS