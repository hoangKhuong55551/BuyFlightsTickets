from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from bookings.models import Booking
from .models import Payment, RefundRequest


@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        if booking.status == "paid" or Payment.objects.filter(booking=booking).exists():
            messages.info(request, "Vé này đã được thanh toán rồi!")
            return redirect("ticket", booking_id=booking.id)
            
        Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            method="mock",
            status="success",
            payment_date=timezone.now()
        )
        booking.status = "paid"
        booking.save()

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

        messages.success(
            request,
            f"Thanh toán thành công! Mã booking: {booking.booking_code}"
        )
        return redirect("ticket", booking_id=booking.id)

    return render(request, "payments/payment.html", {"booking": booking})


@login_required
def request_refund(request, booking_id):
    """Trang yêu cầu hoàn tiền cho booking đã thanh toán."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Kiểm tra điều kiện
    can, error_msg = RefundRequest.can_request(booking)
    if not can:
        messages.error(request, error_msg)
        return redirect("my_bookings")

    # Tính số tiền hoàn
    refund_amount = RefundRequest.calc_refund_amount(booking)

    # Xác định % hoàn tiền để hiển thị cho user
    if booking.flight:
        now = timezone.now()
        hours_left = (booking.flight.departure_time - now).total_seconds() / 3600
        if hours_left > 24:
            refund_pct = 100
        elif hours_left > 2:
            refund_pct = 50
        else:
            refund_pct = 0
    else:
        hours_left = None
        refund_pct = 100

    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()

        # Tạo RefundRequest
        RefundRequest.objects.create(
            booking=booking,
            refund_amount=refund_amount,
            reason=reason,
            status="pending",
        )

        messages.success(
            request,
            f"Yêu cầu hoàn tiền {refund_amount:,.0f} đ cho booking "
            f"{booking.booking_code} đã được gửi. Admin sẽ xử lý trong 1-3 ngày làm việc."
        )
        return redirect("my_bookings")

    context = {
        "booking": booking,
        "refund_amount": refund_amount,
        "refund_pct": refund_pct,
        "hours_left": hours_left,
    }
    return render(request, "payments/refund_request.html", context)
