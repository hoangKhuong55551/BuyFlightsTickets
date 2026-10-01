import re
with open('NguyenNgocHoangKhuong_CNPM24CT1/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()
if 'dashboard.urls' not in text:
    text = text.replace('    path(', '    path("dashboard/", include("dashboard.urls")),\n    path(')
    with open('NguyenNgocHoangKhuong_CNPM24CT1/urls.py', 'w', encoding='utf-8') as f:
        f.write(text)
