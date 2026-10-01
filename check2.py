from html.parser import HTMLParser
import re

class Linter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
    def handle_starttag(self, tag, attrs):
        attr_names = [a[0] for a in attrs]
        if len(attr_names) != len(set(attr_names)):
            self.errors.append(f'Duplicate attributes in <{tag}> at line {self.getpos()[0]}')

p = Linter()
with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()
# strip django template logic
text = re.sub(r'{%[^\}]*%}', '', text)
text = re.sub(r'{{[^\}]*}}', '', text)
p.feed(text)
print("Errors:", p.errors)
