import os
import smtplib
from email.mime.text import MIMEText

try:
    print("Testing SMTP...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.starttls()
    server.login('khuong206111@gmail.com', 'xcehlqdxorujvxgf')
    print("Login successful!")
    
    msg = MIMEText('Test email from SkyBook')
    msg['Subject'] = 'Test SkyBook'
    msg['From'] = 'SkyBook Airlines <khuong206111@gmail.com>'
    msg['To'] = 'khuong206111@gmail.com'
    
    server.send_message(msg)
    print("Email sent successfully!")
    server.quit()
except Exception as e:
    print(f"Error: {e}")
