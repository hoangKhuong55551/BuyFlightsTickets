import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email_bg(to_email, subject, html_content):
    """Gửi email thông qua cấu hình SMTP của Django trong background thread."""
    def _send():
        try:
            # Lấy thông tin người gửi từ settings
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'SkyBook <noreply@skybook.vn>')
            
            # Tạo email (bản text thuần và bản HTML)
            msg = EmailMultiAlternatives(
                subject=subject,
                body="Vui lòng bật chế độ hiển thị HTML để xem nội dung email này.",
                from_email=from_email,
                to=[to_email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print("\n" + "="*50)
            print(f"⚠️ KHÔNG THỂ GỬI EMAIL TỚI: {to_email}")
            print(f"LỖI SMTP: {e}")
            print("="*50 + "\n")
            
    threading.Thread(target=_send).start()
