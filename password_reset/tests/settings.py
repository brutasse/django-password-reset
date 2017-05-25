ROOT_URLCONF = 'password_reset.tests.urls'

SECRET_KEY = 'yo secret yo'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'password_reset.sqlite',
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'password_reset',
    'password_reset.tests',
)

MIDDLEWARE = []

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'OPTIONS': {
        'loaders': (
            'django.template.loaders.app_directories.Loader',
        ),
    },
}]
