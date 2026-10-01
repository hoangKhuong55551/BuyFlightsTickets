import re
with open('NguyenNgocHoangKhuong_CNPM24CT1/settings.py', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('    "recommendations",\n\n    \'django.contrib.admin\',', '    "recommendations",\n    "dashboard",\n\n    \'django.contrib.admin\',')
with open('NguyenNgocHoangKhuong_CNPM24CT1/settings.py', 'w', encoding='utf-8') as f:
    f.write(text)
