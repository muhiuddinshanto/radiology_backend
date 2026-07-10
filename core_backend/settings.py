import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
import dj_database_url  # নতুন যোগ করা হয়েছে

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security-critical settings environment variable থেকে আসে ──
# Locally: .env ফাইল থেকে পড়া হয়।
# Render/Railway/PythonAnywhere-এ: platform-এর "Environment Variables"
# ড্যাশবোর্ডে সেট করতে হবে — real value কখনো git-এ commit করবেন না।
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-dev-only')
DEBUG = config('DEBUG', default=False, cast=bool)

# ⚠️ default-এ 'your-app-name.onrender.com' শুধু placeholder — deploy করার পর
# Render dashboard-এর Environment ট্যাবে ALLOWED_HOSTS env var-এ আপনার
# actual domain (যেমন radiology-backend-do2p.onrender.com) বসাতে হবে।
# comma দিয়ে একাধিক host দেওয়া যায়: "domain1.com,domain2.com"
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=Csv()
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # Local Apps
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# ── Middleware order গুরুত্বপূর্ণ ──
# WhiteNoise SecurityMiddleware-এর ঠিক পরে বসাতে হয় (Django-র official
# recommendation), আর CorsMiddleware CommonMiddleware-এর আগে থাকা উচিত।
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core_backend.urls'

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

WSGI_APPLICATION = 'core_backend.wsgi.application'

# ── Database ──
# dj_database_url.config() Render-এর দেওয়া DATABASE_URL env var থেকে
# Postgres কনফিগ পড়বে। env var না থাকলে (লোকাল dev) sqlite3 fallback হবে।
# conn_max_age কানেকশন পুল করে পারফরম্যান্স ভালো করে,
# ssl_require Render-এর Postgres-এর জন্য প্রয়োজন (তারা SSL বাধ্যতামূলক করে)।
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ── Static files (CSS, JS, Django admin assets) ──
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic এখানে ফাইল জড়ো করবে

# WhiteNoise-কে বলা হচ্ছে static file compress + hash করে cache-friendly
# filename দিতে, আর নিজে থেকেই সেগুলো serve করতে (DEBUG=False অবস্থায়ও)।
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True

# ── Media files (user-uploaded images) ──
# ⚠️ এটা শুধু LOCAL DEV-এর জন্য কাজ করে। DEBUG=False (production) হলে
# urls.py-এর static() হেল্পার কোনো URL pattern যোগ করে না, ফলে এই path
# দিয়ে media serve হবে না, আর Render-এর মতো ephemeral filesystem-এ
# redeploy হলে uploaded file হারিয়েও যেতে পারে।
# প্রোডাকশনের জন্য django-storages + S3/Cloudinary-জাতীয় cloud storage
# ব্যবহার করা দরকার — এই সেটিংস ফাইলে এখনো সেটা যোগ করা হয়নি।
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'