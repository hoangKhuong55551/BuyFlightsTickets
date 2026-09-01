import re

with open('payments/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('from django.core.mail import send_mail', 'from django.core.mail import EmailMultiAlternatives\nfrom django.template.loader import render_to_string')

old_send = re.search(r'send_mail\([\s\S]*?fail_silently=True,\n\s*\)', content)

new_send = """
        # Gửi email xác nhận kèm E-Ticket HTML
        subject = f"SkyBook - Xác nhận đặt vé {booking.booking_code}"
        from_email = None
        to_email = booking.user.email or "noreply@dev.null"
        
        context = {"booking": booking}
        text_content = render_to_string("emails/ticket_email.txt", context)
        html_content = render_to_string("emails/ticket_email.html", context)
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
"""

if old_send:
    content = content.replace(old_send.group(0), new_send.strip())
    with open('payments/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Success")
else:
    print("Not found")
