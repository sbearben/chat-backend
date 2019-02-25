"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 10.0.2.2 is the address used by the Android Emulator for the localhost
ALLOWED_HOSTS = ['127.0.0.1', '10.0.2.2']


# Application definition

INSTALLED_APPS = [
    'channels',
    # My apps
    'chat',
    'user',
    'realtime',
    'friendships',
    # Django/REST stuff
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # For tokens
    'rest_framework.authtoken',
    # For login/logout and other stuff
    'rest_auth',
    # For registration (both normal and social)
    'django.contrib.sites',
    'allauth',
    'allauth.account',

    # have to add this because there is a bug that causes an error when trying to delete a user if this isn't added
    # see: https://github.com/Tivix/django-rest-auth/issues/412
    'allauth.socialaccount',

    'rest_auth.registration',
    # For adding/following friends and such
    'friendship',
]

# This is part of the installation instructions for user registration
SITE_ID = 1
# This is also needed for user registration (since it needs the setting for how to send a registration confirmation email)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # The following is required for the sqlite3 database to work correctly during tests
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3')
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


# Custom user
AUTH_USER_MODEL = 'user.CustomUser'


# Channels
ASGI_APPLICATION = 'mysite.routing.application'
# Configure the channel layer - the layer allows multiple channels (every consumer
# instance has an auto generated unique channel name) to communicate with each other
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            # 6379 is the port number we started the Redis server on earlier with the command: docker run -p 6379:6379 -d redis:2.8
            "hosts": [('127.0.0.1', 6379)], 
        }
    }
}

# Rest Framework - settings for pagination
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Rest-Auth Framework - Custom serializers
REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'common.serializers.TokenSerializer',
}


##### Project-specific settings

MSG_TYPE_MESSAGE = 0  # For standard messages
MSG_TYPE_TYPING_START = 1  # For when a user starts typing a message
MSG_TYPE_TYPING_STOP = 2  # For when a user stops typing a message
MSG_TYPE_FRIENDSHIP_REQUEST = 3  # For when a user receives a friend request
MSG_TYPE_NEW_FRIEND = 4  # For when a user gets a new friend (i.e. a friendship request is accepted)
MSG_TYPE_FRIEND_REMOVED = 5  # For when a user removes a friend
MSG_TYPE_ERROR = 6  # For errors

MESSAGE_TYPES_CHOICES = (
    (MSG_TYPE_MESSAGE, 'MESSAGE'),
    (MSG_TYPE_TYPING_START, 'TYPING_START'),
    (MSG_TYPE_TYPING_STOP, 'TYPING_STOP'),
    (MSG_TYPE_FRIENDSHIP_REQUEST, 'FRIENDSHIP_REQUEST'),
    (MSG_TYPE_NEW_FRIEND, 'NEW_FRIEND'),
    (MSG_TYPE_FRIEND_REMOVED, 'FRIEND_REMOVED'),
    (MSG_TYPE_ERROR, 'ERROR'),
)

MESSAGE_TYPES_LIST = [
    MSG_TYPE_MESSAGE,
    MSG_TYPE_TYPING_START,
    MSG_TYPE_TYPING_STOP,
    MSG_TYPE_FRIENDSHIP_REQUEST,
    MSG_TYPE_NEW_FRIEND,
    MSG_TYPE_FRIEND_REMOVED,
    MSG_TYPE_ERROR,
]
