
with open('templates/bookings/change_seat.html', 'r', encoding='utf-8') as f:
    text = f.read()

def un_cp1252(text):
    # Convert string back to bytes using cp1252 logic
    # characters from 0-255 are mostly 1:1 except for the windows-1252 specific ones
    cp1252_decoding_map = {
        0x80: '\u20ac', 0x82: '\u201a', 0x83: '\u0192', 0x84: '\u201e', 0x85: '\u2026',
        0x86: '\u2020', 0x87: '\u2021', 0x88: '\u02c6', 0x89: '\u2030', 0x8a: '\u0160',
        0x8b: '\u2039', 0x8c: '\u0152', 0x8e: '\u017d',
        0x91: '\u2018', 0x92: '\u2019', 0x93: '\u201c', 0x94: '\u201d', 0x95: '\u2022',
        0x96: '\u2013', 0x97: '\u2014', 0x98: '\u02dc', 0x99: '\u2122', 0x9a: '\u0161',
        0x9b: '\u203a', 0x9c: '\u0153', 0x9e: '\u017e', 0x9f: '\u0178'
    }
    reverse_map = {v: k for k, v in cp1252_decoding_map.items()}
    
    b = bytearray()
    for char in text:
        if char in reverse_map:
            b.append(reverse_map[char])
        elif ord(char) < 256:
            b.append(ord(char))
        else:
            # If there's some other weird char, just put a question mark or keep it
            print(f'Warning: unknown char {repr(char)}')
            b.append(ord('?'))
    return bytes(b)

try:
    raw_bytes = un_cp1252(text)
    fixed_text = raw_bytes.decode('utf-8')
    with open('templates/bookings/change_seat_fixed.html', 'w', encoding='utf-8') as f:
        f.write(fixed_text)
    print('Fixed successfully!')
except Exception as e:
    print(f'Error: {e}')

