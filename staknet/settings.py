from pathlib import Path
import environ
import os
import mongoengine

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'staknet.urls'

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

WSGI_APPLICATION = 'staknet.wsgi.application'

# Mongoengine connection
MONGODB = env("MONGO_INITDB_DATABASE")
MONGODB_HOST = env("MONGO_INITDB_HOST")
MONGODB_PORT = int(env("MONGO_INITDB_PORT"))
MONGODB_USERNAME = env("MONGO_INITDB_ROOT_USERNAME")
MONGODB_PASSWORD = env("MONGO_INITDB_ROOT_PASSWORD")

mongoengine.connect(
    db=MONGODB,
    host=MONGODB_HOST,
    port=MONGODB_PORT,
    username=MONGODB_USERNAME,
    password=MONGODB_PASSWORD,
    alias='default',
)

# mongoengine.connect(
#     db=env("MONGO_INITDB_DATABASE"),
#     host=env("MONGO_INITDB_HOST"),
#     port=int(env("MONGO_INITDB_PORT")),
#     username=env("MONGO_INITDB_ROOT_USERNAME"),
#     password=env("MONGO_INITDB_ROOT_PASSWORD"),
#     alias='stakDB'
# )

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.auth.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'core.auth.AuthPermission'
    ),
}


# JWT settings
JWT_EXPIRATION_MINUTE = 60  # JWT token expiration time in minutes
ENCRYPT_ALGORITHM = 'HS256'  # JWT token encryption algorithm


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": env("LOG_LEVEL"),
            "class": "logging.FileHandler",
            "filename": env("LOG_FILE_PATH"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": env("LOG_LEVEL"),
            "propagate": True,
        },
    },
}
