import os
from pathlib import Path

# 프로젝트 베이스 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 보안 관련
SECRET_KEY = 'django-insecure-your-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

# 애플리케이션 정의
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Classify',  # 너의 앱 이름
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Wound_Classify.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # 앱 내부 templates 디렉토리 사용
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

WSGI_APPLICATION = 'Wound_Classify.wsgi.application'

# 데이터베이스 설정 (기본 SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 비밀번호 검증
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

# 국제화
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# 정적 파일 설정
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'Classify/static']

# 미디어 파일 설정 (필요할 경우)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 기본 자동 필드 타입
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
