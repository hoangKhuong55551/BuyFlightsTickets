from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from bookings.models import Booking
from .models import Payment


@login_required(login_url="/users/login/")
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
            subject=f"Xac nhan dat ve — {booking.booking_code}",
            message=(
                f"Xin chao {booking.user.username},\n\n"
                f"Dat ve cua ban da thanh cong!\n"
                f"Ma booking: {booking.booking_code}\n"
                f"Tong tien: {booking.total_price} VND\n\n"
                f"Cam on ban da su dung dich vu Flight Booking."
            ),
            from_email="noreply@flightbooking.com",
            recipient_list=[booking.user.email or "noreply@dev.null"],
            fail_silently=True,
        )

        messages.success(
            request,
            f"Thanh toan thanh cong! Ma booking: {booking.booking_code}"
        )
        return redirect("ticket", booking_id=booking.id)

    return render(request, "payments/payment.html", {"booking": booking})
