with open('NguyenNgocHoangKhuong_CNPM24CT1/settings.py', 'rb') as f:
    content = f.read()
idx = content.find(b'# \xe2\x94\x80\xe2\x94\x80 Session')
if idx != -1:
    clean_content = content[:idx].decode('utf-8')
    with open('NguyenNgocHoangKhuong_CNPM24CT1/settings.py', 'w', encoding='utf-8') as f:
        f.write(clean_content + '''# ── Session ─────────────────────────────────────────────────────────────────
SESSION_COOKIE_AGE = 3600  # 1 giờ
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_LOGIN_ON_GET = True
''')
