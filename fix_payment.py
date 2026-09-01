import re

with open('payments/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add a check for booking.status == "paid" to prevent IntegrityError
check_paid = """
    if request.method == "POST":
        if booking.status == "paid" or Payment.objects.filter(booking=booking).exists():
            messages.info(request, "Vé này đã được thanh toán rồi!")
            return redirect("ticket", booking_id=booking.id)
"""

content = content.replace('    if request.method == "POST":', check_paid.lstrip())

with open('payments/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated views.py")
