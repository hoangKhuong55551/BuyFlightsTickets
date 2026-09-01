import os

with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add WhiteNoise Middleware
if "WhiteNoiseMiddleware" not in content:
    content = content.replace(
        "'django.middleware.security.SecurityMiddleware',",
        "'django.middleware.security.SecurityMiddleware',\n    'whitenoise.middleware.WhiteNoiseMiddleware',"
    )

# 2. Add STATIC_ROOT
if "STATIC_ROOT" not in content:
    content = content.replace(
        "STATIC_URL = 'static/'",
        "STATIC_URL = 'static/'\nSTATIC_ROOT = BASE_DIR / 'staticfiles'"
    )

# 3. Add dj_database_url
import_db = "import dj_database_url\n"
if "import dj_database_url" not in content:
    content = import_db + content
    
db_config = """DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}"""

import re
content = re.sub(r'DATABASES = \{[\s\S]*?\}', db_config, content, count=1)

# 4. Update ALLOWED_HOSTS for Render
content = content.replace("ALLOWED_HOSTS=127.0.0.1,localhost", "ALLOWED_HOSTS=*")
content = content.replace("ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())", "ALLOWED_HOSTS = ['*']") # Just allow all for quick test

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated settings.py")
