from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from bookings.models import Booking
from .models import Payment, RefundRequest


@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            method="mock",
            status="success",
            payment_date=timezone.now()
        )
        booking.status = "paid"
        booking.save()

        send_mail(
            subject=f"Xác nhận đặt vé — {booking.booking_code}",
            message=(
                f"Xin chào {booking.user.username},\n\n"
                f"Đặt vé của bạn đã thành công!\n"
                f"Mã booking: {booking.booking_code}\n"
                f"Tổng tiền: {booking.total_price:,.0f} VNĐ\n\n"
                f"Cảm ơn bạn đã sử dụng SkyBook."
            ),
            from_email=None,
            recipient_list=[booking.user.email or "noreply@dev.null"],
            fail_silently=True,
        )

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
            f"Yêu cầu hoàn tiền {refund_amount:,.0f} ₫ cho booking "
            f"{booking.booking_code} đã được gửi. Admin sẽ xử lý trong 1–3 ngày làm việc."
        )
        return redirect("my_bookings")

    context = {
        "booking": booking,
        "refund_amount": refund_amount,
        "refund_pct": refund_pct,
        "hours_left": hours_left,
    }
    return render(request, "payments/refund_request.html", context)

