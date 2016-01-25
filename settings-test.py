#import environ
#env = environ.Env()

DEBUG=True
USE_TZ=True

DATABASES={
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

ROOT_URLCONF="portfolio.urls"

INSTALLED_APPS=[
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.humanize",
    "portfolio",
    "currency_history",
    "pjcore",
]
SITE_ID=1
MIDDLEWARE_CLASSES=()
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': ('app_namespace.Loader',
                        'django.template.loaders.app_directories.Loader')
        }
    }
]
SECRET_KEY='a#~586)qt%,Bs\VH?4u%G(*mtHs@;*&=6>l/~h6}'
#SECRET_KEY = env("DJANGO_SECRET_KEY")
