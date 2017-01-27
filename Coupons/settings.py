import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!n%1x%$g47406bb6y(u_+@23h+(tob)r!05bt7r-*88qn$e3o6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

#Próbowałem dodać moduł statystyk, jednak nie udało mi się rozwiązać problemów, które pojawiają się po edycji poniższych plików.

#ADMIN_TOOLS_INDEX_DASHBOARD = 'Coupons.dashboard.CustomIndexDashboard'
#ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'Coupons.dashboard.CustomAppIndexDashboard'

#Session
TIME = 60*10
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = TIME
SESSION_IDLE_TIMEOUT = TIME

#Newsletter confirmation disabled let send e-mail to all users.
NEWSLETTER_CONFIRM_EMAIL = False

# Application definition
INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'django_nvd3',
    'djangobower',
    'django_extensions',
    'admin_tools_stats',
    'events',
    'contact_form',
    'tinymce',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'sorl.thumbnail',
    'newsletter',
    'django_comments',
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Coupons.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'django.template.loaders.eggs.Loader',
                    'admin_tools.template_loaders.Loader',
                ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'Coupons.wsgi.application'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'pl-PL'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_FINDERS = \
    ('djangobower.finders.BowerFinder',
     "django.contrib.staticfiles.finders.FileSystemFinder",
     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
     )

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'Coupons/images/')

#E-mail address
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mailtrap.io'
EMAIL_HOST_USER = '09205445f31e72'
EMAIL_HOST_PASSWORD = '2977e2646233dd'
EMAIL_PORT = '465'


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)
# Specifie path to components root (you need to use absolute path)
BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

BOWER_PATH = '/usr/local/bin/bower'

BOWER_INSTALLED_APPS = (
    'jquery#2.0.3',
    'jquery-ui#~1.10.3',
    'd3#3.3.6',
    'nvd3#1.1.12-beta',
)

#IMPORT LOCAL SETTINGS
#=====================
try:
    from settings_local import *
except ImportError:
    pass
