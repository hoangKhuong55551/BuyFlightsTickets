import re
with open('dashboard/views.py', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('created_at__gte', 'booking_date__gte').replace('created_at__lt', 'booking_date__lt')
with open('dashboard/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
