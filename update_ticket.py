import re

with open('templates/bookings/ticket.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """
        {% for t in booking.tickets.all %}
        <div class="bp-passenger-row">
          <span style="font-weight:600;">{{ t.passenger.full_name }}</span>
          <span>Gh <strong style="color:var(--blue);font-size:1.05rem;">{{ t.seat_number }}</strong></span>
        </div>
        {% endfor %}
"""
old_block_cleaned = re.sub(r'\s+', ' ', old_block.strip())
content_cleaned = re.sub(r'\s+', ' ', content)

# Instead of complex regex, let's just do a manual replace in Python using simple string match
import sys

def replace_seat_block():
    with open('templates/bookings/ticket.html', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    for i, line in enumerate(lines):
        if "t.seat_number" in line and "bp-passenger-row" in lines[i-2]:
            lines[i] = '          <div><span>Ghế <strong style="color:var(--blue);font-size:1.05rem;margin-right:12px;">{{ t.seat_number }}</strong></span><a href="{% url \'change_seat\' t.id %}" style="display:inline-block; padding: 4px 10px; font-size: 0.7rem; border-radius: 99px; border: 1px solid var(--border); text-decoration: none; font-weight: bold; color: var(--navy);">Đổi ghế</a></div>\n'
            
    with open('templates/bookings/ticket.html', 'w', encoding='utf-8') as file:
        file.writelines(lines)
        
replace_seat_block()
