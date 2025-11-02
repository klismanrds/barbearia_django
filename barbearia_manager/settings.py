import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-voi5l07=k4ltg5+^_wo93jx*7fbmd-^6^rg(mlprxyzg(i)x7s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

LOCAL = os.environ.get('LOCAL', 'True') == 'True' 

if LOCAL:
    DEBUG = True
    # O ALLOWED_HOSTS é ignorado quando DEBUG é True
    ALLOWED_HOSTS = ['*'] 
else:
    # Configurações de PRODUÇÃO
    DEBUG = False
    
    # Adiciona o domínio do Railway (e o seu customizado, se houver)
    ALLOWED_HOSTS = [
        '.railway.app', # Para o subdomínio gerado
        '127.0.0.1', 
        'localhost',
        "ze.localhost",
         "alfa.localhost",
        # 'seumaiordomínio.com' # Se estiver usando um domínio próprio
    ]
# ----------------------------------------------------
DATABASE_URL = os.environ.get('DATABASE_URL')

if not LOCAL and DATABASE_URL:
    # Configuração de PRODUÇÃO: Usa a URL do Railway
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Configuração de DESENVOLVIMENTO: Usa o SQLite ou PostgreSQL local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Ou 'django.db.backends.postgresql'
            'NAME': BASE_DIR / 'db.sqlite3',
            # ... suas outras configurações locais
        }
    }
# ----------------------------------------------------

# 1. APPS Comuns e de Tenant
SHARED_APPS = [
    'django_tenants',  # Deve vir primeiro!
    'tenants',         # O app 'tenants' que criamos
    'django.contrib.contenttypes',
    'usuarios',
    'crispy_forms',
    'crispy_bootstrap5',
    'django.contrib.humanize',
    'django_extensions',
    # ... (outros apps do Django, exceto 'auth' e 'sessions')
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

AUTH_USER_MODEL = 'usuarios.Usuario'

TENANT_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'servicos',
    'barbeiros',
    'clientes',
    'agendamentos',
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]
# 2. Configurações de Tenant
TENANT_MODEL = "tenants.Barbearia" # Seu modelo de tenant
DEFAULT_TENANT_SCHEMA = "public" # Schema padrão (para dados globais)
TENANT_DOMAIN_MODEL = 'tenants.Domain'

MIDDLEWARE = [
    'django_tenants.middleware.TenantMiddleware', # Deve vir primeiro!
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'barbearia_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'barbearia_manager.wsgi.application'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'barbearia_db',  # Nome do seu DB
        'USER': 'klismanrds',  # Seu usuário
        'PASSWORD': '32166096',  # Sua senha
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# --- Adicione esta configuração ---
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)
# --

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
