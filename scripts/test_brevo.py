
import urllib.request
import json
import os
from decouple import config

key = config('BREVO_API_KEY', default='')

print(f'Testing with Key: {key[:15]}...')

url = 'https://api.brevo.com/v3/smtp/email'
headers = {
    'accept': 'application/json',
    'api-key': key,
    'content-type': 'application/json'
}
data = {
    'sender': {'name': 'SkyBook Airlines', 'email': 'khuong206111@gmail.com'},
    'to': [{'email': 'khuong206111@gmail.com'}],
    'subject': 'Test Brevo API',
    'htmlContent': '<p>This is a test from Brevo</p>'
}

try:
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req) as response:
        print('Success:', response.read().decode())
except Exception as e:
    print('Error:', e)
    if hasattr(e, 'read'):
        print('Details:', e.read().decode())

