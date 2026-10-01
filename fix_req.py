with open('requirements.txt', 'rb') as f:
    text = f.read().decode('utf-8', errors='ignore')
text = text.replace('\x00', '')
with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(text.strip() + '\n')
