from pathlib import Path
from decouple import config
from datetime import timedelta
from rest_framework.settings import api_settings

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY", cast=str)

DEBUG = config("DEBUG", cast=bool)
ALLOWED_HOSTS = [config("ALLOWED_HOST_A", cast=str),
                 config("ALLOWED_HOST_B", cast=str)]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "rest_framework",
    "knox",

    # apps
    "audits.apps.AuditsConfig",
    "authentication.apps.AuthenticationConfig",
    "bookings.apps.BookingsConfig",
    "countries.apps.CountriesConfig",
    "genders.apps.GendersConfig",
    "maps.apps.MapsConfig",
    "profiles.apps.ProfilesConfig",
    "users.apps.UsersConfig",
    "wallets.apps.WalletsConfig",

]

# rest framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),

}

# user model
AUTH_USER_MODEL = "users.CustomUser"

REST_KNOX = {
    "SECURE_HASH_ALGORITHM": config("SECURE_HASH_ALGORITHM", cast=str),
    "AUTH_TOKEN_CHARACTER_LENGTH": config("AUTH_TOKEN_CHARACTER_LENGTH", cast=int),
    "TOKEN_TTL": timedelta(hours=1),
    "USER_SERIALIZER": "users.serializers.UserSerializer",
    "TOKEN_LIMIT_PER_USER": config("TOKEN_LIMIT_PER_USER", cast=int),
    "AUTO_REFRESH": config("AUTO_REFRESH", cast=bool,),
    "EXPIRY_DATETIME_FORMAT": config("EXPIRY_DATETIME_FORMAT", cast=str),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xiaoma.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'xiaoma.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = config("LANGUAGE_CODE", cast=str)
TIME_ZONE = config("TIME_ZONE", cast=str)
USE_I18N = config("USE_I18N", cast=bool)
USE_TZ = config("USE_TZ", cast=str)

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# gdal settings
GDAL_LIBRARY_PATH = r'C:\\OSGeo4W\bin\\gdal306.dll'
