import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Your secret key here
SECRET_KEY = '<Secret-Key>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

QA_SETTINGS = {
    'qa_messages': True,
    'qa_description_optional': False,
    'reputation': {
        'CREATE_QUESTION': 0,
        'CREATE_ANSWER': 0,
        'CREATE_ANSWER_COMMENT': 0,
        'CREATE_QUESTION_COMMENT': 0,
        'ACCEPT_ANSWER': 0,
        'UPVOTE_QUESTION': 0,
        'UPVOTE_ANSWER': 0,
        'DOWNVOTE_QUESTION': 0,
        'DOWNVOTE_ANSWER': 0,
    }
}


INSTALLED_APPS = [
    'accounts',
    'qa',
    'taggit',
    'hitcount',
    'markdownx',
    'star_ratings',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django', # For All Social Authentication
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware', # For All Social Authentication
]

ROOT_URLCONF = 'ideate2018.urls'

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
                # For All Social Authentication
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'ideate2018.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'ideate2018/../accounts/media')

# when you log in you visit your account profile page
LOGIN_REDIRECT_URL = '/account/'
LOGIN_URL = '/account/login/'
# For mailing purposes

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# For Github Authentication

SOCIAL_AUTH_GITHUB_KEY = '1872ea14c197d599ebe5'
SOCIAL_AUTH_GITHUB_SECRET = 'cc56899a4a0cf19258c33d76280450f9be98ad46'

# For the Rating Application
STAR_RATINGS_RERATE = False
STAR_RATINGS_RANGE = 8
STAR_RATINGS_ANONYMOUS = True
STAR_RATINGS_STAR_HEIGHT = 16
STAR_RATINGS_STAR_WIDTH =  16
