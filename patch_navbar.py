import re
with open('templates/partials/navbar.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '''{% if user.is_staff or user.is_superuser %}''',
    '''{% if user.is_staff or user.is_superuser or user.profile.managed_airline %}
          <li><a href="{% url 'dashboard_home' %}">Dashboard</a></li>'''
)
with open('templates/partials/navbar.html', 'w', encoding='utf-8') as f:
    f.write(text)
