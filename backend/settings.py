import os
import dj_database_url
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [
    os.getenv("ALLOWED_HOSTS", "localhost"),
    'kakeibo-backend.onrender.com',
    'localhost',
]

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'rest_framework','corsheaders', 'accounts', 'ledger',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
WSGI_APPLICATION = 'backend.wsgi.application'

CORS_ALLOWED_ORIGINS = [
    "https://watababekakeibo.netlify.app ",
    "http://localhost:5173",
]

DATABASES = {
    "default": dj_database_url.parse(
        os.getenv("DATABASE_URL", "sqlite:///db.sqlite3"),
        conn_max_age=600,
    )
}

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "accounts.auth.AppJWTAuthentication", 
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}