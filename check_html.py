import re, collections
with open('templates/home.html', 'r', encoding='utf-8') as f:
    content = f.read()
ids = re.findall(r'id=[\"\']([^\"\']+)[\"\']', content)
c = collections.Counter(ids)
for k, v in c.items():
    if v > 1:
        print('Duplicate ID:', k, v)
