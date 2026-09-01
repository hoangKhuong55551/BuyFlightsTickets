import re

with open('templates/bookings/change_seat.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the inline style
# 1. Remove the inline style from .plane-fuselage
content = re.sub(r'<div class="plane-fuselage" style="[^>]+>', '<div class="plane-fuselage">', content)

# 2. Add .plane-wings div above .plane-fuselage
content = content.replace('<div class="plane-fuselage">', '<div class="plane-wings"></div>\n        <div class="plane-fuselage">')

# 3. Add the plane-wings styling to the <style> block
svg_style = """
.plane-wings { position: absolute; top: 300px; left: 50%; transform: translateX(-50%); width: 900px; height: 400px; z-index: 0; pointer-events: none; background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400"><path d="M 340 100 L 50 300 Q 20 310 30 330 L 340 260 Z" fill="%23ffffff" opacity="0.6"/><rect x="220" y="220" width="50" height="90" rx="25" fill="%23ffffff" opacity="0.7"/><path d="M 660 100 L 950 300 Q 980 310 970 330 L 660 260 Z" fill="%23ffffff" opacity="0.6"/><rect x="730" y="220" width="50" height="90" rx="25" fill="%23ffffff" opacity="0.7"/></svg>') no-repeat center center; background-size: contain; }
"""

# Replace the empty .plane-wings definition with the full one
content = re.sub(r'\.plane-wings \{[^\}]+\}', svg_style.strip(), content)

with open('templates/bookings/change_seat.html', 'w', encoding='utf-8') as f:
    f.write(content)
