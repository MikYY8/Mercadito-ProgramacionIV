from pathlib import Path
import environ
import os
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env()  # lee .env si existe
 
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env("SECRET_KEY", default="dev-secret-no-usar-en-prod")
DEBUG = env("DEBUG", default=True)
ALLOWED_HOSTS = ["*"]
MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
MERCADOPAGO_PUBLIC_KEY = os.getenv("MERCADOPAGO_PUBLIC_KEY")

BASICS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"django.contrib.sites", 
    ]

TERCEROS = [
	"allauth", 
	"allauth.account", 
	"allauth.socialaccount", 
	"allauth.socialaccount.providers.google",
	"allauth.socialaccount.providers.github",
	"rest_framework",
    "drf_yasg",
]

PROPIAS = [
	"core",
    "market",
    "perfil",
    "market_ai",
	"presence",
    "simple_chat",
    "quotes",
]

INSTALLED_APPS = BASICS + TERCEROS + PROPIAS
 
SITE_ID = 1
 
AUTHENTICATION_BACKENDS = [
	"django.contrib.auth.backends.ModelBackend",
	"allauth.account.auth_backends.AuthenticationBackend",
]
 
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
 
# (opcional) Config de allauth
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

SESSION_COOKIE_AGE = 30 * 60           # 30 minutos (en segundos)
SESSION_SAVE_EVERY_REQUEST = True      # cada request renueva el tiempo
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
    "presence.middleware.AutoLogoutMiddleware",
	"presence.middleware.UpdateLastSeenMiddleware"
]
 
ROOT_URLCONF = "config.urls"
 
TEMPLATES = [
	{
    	"BACKEND": "django.template.backends.django.DjangoTemplates",
    	"DIRS": [BASE_DIR / "templates"], 	# <-- carpeta de templates
    	"APP_DIRS": True,
    	"OPTIONS": {
        	"context_processors": [
                "django.template.context_processors.csrf", #solo esto para formularios
            	"django.template.context_processors.debug",
            	"django.template.context_processors.request",  # <-- requerido por allauth
            	"django.contrib.auth.context_processors.auth",
            	"django.contrib.messages.context_processors.messages",
        	],
    	},
	},
]
 
WSGI_APPLICATION = "config.wsgi.application"
 
DATABASES = {
	"default": {
    	"ENGINE": "django.db.backends.sqlite3",
    	"NAME": BASE_DIR / "db.sqlite3",
	}
}

SOCIALACCOUNT_PROVIDERS = {
        "google": {
        "APP": {
            "client_id": "1025172031933-7gv483i7kpij9en47vtidma82r81oa9d.apps.googleusercontent.com", # claves google
            "secret": "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",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    },
    "github": {
        "APP": {
            "client_id": "Ov23li52R2sRyjhsJdYh",   # claves github
            "secret": "b11c1555a6357567d2f1b165cd438d94c38ff08e",
        },
        "SCOPE": ["user:email"],
    },
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)