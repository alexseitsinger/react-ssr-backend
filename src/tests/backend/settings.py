import os

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

SECRET_KEY = "secret-key-213213"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BACKEND_DIR, "templates")],
        "APP_DIRS": True,
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test",
        "HOST": "127.0.0.101",
        "PORT": 5432,
        "USER": "main",
        "PASSWORD": "test",
    }
}

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "dist/",
        "STATS_FILE_TIMEOUT": 10,
        "STATS_FILE": "http://127.0.0.102:3000/stats/client/development",
    }
}

REACT_SSR = {
    "RENDER": {
        "TEMPLATE_NAME": "index.html",
        "URL": "http://127.0.0.102:3000/render",
        "TIMEOUT": 5.0,
        "HEADERS": {"Content-Type": "application/json"},
    },
    "STATE": {
        "URL": "http://127.0.0.102:3000/state",
        "TIMEOUT": 5.0,
        "HEADERS": {"Content-Type": "application/json"},
        "CORE": {
            "NAME": "core",
            "USER_SERIALIZER": None,
            "USER_PATH": "core.authentication.user",
            "TOKENS_KEY": "core.authentication.tokens",
        },
    },
    "SECRET_KEY": {"VALUE": "THIS_IS_A_SECRET_KEY", "HEADER_NAME": "secret-key"},
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "react_ssr",
    "webpack_loader_remote",
    "src.tests",
]
