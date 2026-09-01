with open('templates/bookings/ticket.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Gh? <strong', 'Ghế <strong')
content = content.replace('>D?i gh?</a>', '>Đổi ghế</a>')
content = content.replace('Gh <strong', 'Ghế <strong')

with open('templates/bookings/ticket.html', 'w', encoding='utf-8') as f:
    f.write(content)
