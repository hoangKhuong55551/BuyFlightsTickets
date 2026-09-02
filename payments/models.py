from django.db import models
from django.utils import timezone
from bookings.models import Booking

class Payment(models.Model):
    METHOD_CHOICES = [
        ("banking", "Banking"),
        ("mock", "Mock Payment"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment", verbose_name="Booking")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, verbose_name="Payment Method")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Status")
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Payment Date")

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return self.booking.booking_code


class RefundRequest(models.Model):
    STATUS_CHOICES = [
        ("pending",  "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="refund_request", verbose_name="Booking")
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name="Requested At")
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="Processed At")
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Refund Amount")
    reason = models.TextField(blank=True, verbose_name="Refund Reason")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True, verbose_name="Status")
    admin_note = models.TextField(blank=True, verbose_name="Admin Note")

    class Meta:
        verbose_name = "Refund Request"
        verbose_name_plural = "Refund Requests"
        ordering = ["-requested_at"]

    def __str__(self):
        return f"Refund #{self.booking.booking_code} - {self.get_status_display()}"

    @staticmethod
    def calc_refund_amount(booking):
        """
        Calculate refund amount based on time left before departure:
          > 24h  = 100% refund
          2h-24h = 50% refund
          < 2h   = 0% refund
        If booking has no flight, 100% refund.
        """
        flight = booking.flight
        if not flight:
            return booking.total_price

        now = timezone.now()
        delta = flight.departure_time - now
        hours_left = delta.total_seconds() / 3600

        if hours_left > 24:
            return booking.total_price                          # 100%
        elif hours_left > 2:
            return (booking.total_price * 50 / 100).quantize(  # 50%
                booking.total_price
            )
        else:
            from decimal import Decimal
            return Decimal("0.00")                              # No refund

    @staticmethod
    def can_request(booking):
        """
        Check if booking is eligible for a refund:
        - Must be 'paid'
        - Must not have an existing RefundRequest
        - If it has a flight, must be > 2 hours before departure
        """
        if booking.status != "paid":
            return False, "Only applicable for paid bookings."
        if hasattr(booking, "refund_request"):
            return False, "A refund request has already been submitted."
        if booking.flight:
            now = timezone.now()
            delta = booking.flight.departure_time - now
            hours_left = delta.total_seconds() / 3600
            if hours_left <= 2:
                return False, "Cannot refund after flight departure or within 2 hours of departure."
        return True, ""

    def approve(self):
        """Approve refund: set booking to cancelled, update processed time."""
        self.status = "approved"
        self.processed_at = timezone.now()
        self.save(update_fields=["status", "processed_at"])

        booking = self.booking
        booking.status = "cancelled"
        booking.save(update_fields=["status"])

        # Send notification email via Resend API
        try:
            to_email = booking.user.email
            if to_email:
                import urllib.request
                import json
                
                from decouple import config
                url = "https://api.brevo.com/v3/smtp/email"
                headers = {
                    "accept": "application/json",
                    "api-key": config("BREVO_API_KEY", default=""),
                    "content-type": "application/json"
                }
                data = {
                    "sender": {"name": "SkyBook Airlines", "email": "khuong206111@gmail.com"},
                    "to": [{"email": to_email}],
                    "subject": f"Refund Successful - {booking.booking_code}",
                    "htmlContent": (
                        f"<p>Hello {booking.user.username},</p>"
                        f"<p>Your refund request has been approved.</p>"
                        f"<p><strong>Booking Code:</strong> {booking.booking_code}<br>"
                        f"<strong>Refund Amount:</strong> {self.refund_amount:,.0f} VND</p>"
                        f"<p>Please allow 3-5 business days for the funds to return to your account.</p>"
                        f"<p>Thank you for using SkyBook.</p>"
                    )
                }
                req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req) as response:
                    pass
        except Exception as e:
            print(f"Brevo Refund Error: {e}")

    def reject(self, note=""):
        """Reject refund."""
        self.status = "rejected"
        self.processed_at = timezone.now()
        if note:
            self.admin_note = note
        self.save(update_fields=["status", "processed_at", "admin_note"])
