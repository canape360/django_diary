from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name: str, default: bool = False) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


def env_list(name: str, default=None):
    if default is None:
        default = []
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    return [x.strip() for x in raw.split(",") if x.strip()]


# ========================
# Security / Debug
# ========================
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

DEBUG = env_bool("DEBUG", default=False)

# Render等のプラットフォーム判定（任意：本番でDEBUG事故を潰す）
# Renderが自動で入れる env を使うなら RENDER=true を設定しておくのがおすすめ
if env_bool("RENDER", default=False):
    DEBUG = False

# ALLOWED_HOSTS（本番で * を許可しない）
# 例: ALLOWED_HOSTS=your-app.onrender.com,yourdomain.com
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")

if DEBUG:
    if not ALLOWED_HOSTS:
        ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
else:
    if not ALLOWED_HOSTS:
        raise RuntimeError("ALLOWED_HOSTS is not set for production")
    if "*" in ALLOWED_HOSTS:
        raise RuntimeError("ALLOWED_HOSTS must not contain '*' in production")

# CSRF trusted origins（Renderのデフォルト + 独自ドメイン対応）
# 例: CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com,https://yourdomain.com
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")
if not DEBUG and not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]


# ========================
# Apps / Middleware
# ========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # static配信
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_diary.urls"
WSGI_APPLICATION = "django_diary.wsgi.application"


# ========================
# Templates
# ========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

LOGIN_REDIRECT_URL = "myapp:wholediary"
LOGOUT_REDIRECT_URL = "myapp:home"


# ========================
# Database
# ========================
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # 開発用（本番は基本 DATABASE_URL を必須にしたいなら raise に変えてOK）
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ========================
# Password validation
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ========================
# i18n / timezone
# ========================
LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True


# ========================
# Static files (WhiteNoise)
# ========================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Django 4.2+ は STORAGES 推奨
if DEBUG:
    STORAGES = {
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
else:
    STORAGES = {
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }


# ========================
# Security headers / cookies (production)
# ========================
if not DEBUG:
    # プロキシ配下のHTTPS終端対策（Renderなど）
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # HTTPSへ強制
    SECURE_SSL_REDIRECT = True

    # Cookie を HTTPS 限定
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Cookie の基本（必要なら調整）
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = False  # Djangoの標準はFalse（JSから読むケース考慮）。基本そのままでOK
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

    # HSTS（最初は短め→慣れたら延ばす）
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "3600"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # 参照元ポリシー
    SECURE_REFERRER_POLICY = "same-origin"

    # クリックジャッキング対策（必要なら DENY でもOK）
    X_FRAME_OPTIONS = "DENY"


# ========================
# Default PK
# ========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ========================
# Logging
# ========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
