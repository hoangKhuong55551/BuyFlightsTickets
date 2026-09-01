import os

with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the hanging closing brace if present
import re
content = re.sub(r'DATABASES = \{[\s\S]*?conn_max_age=600\n    \)\n\}\n\}', """DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}""", content)

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed settings.py")
