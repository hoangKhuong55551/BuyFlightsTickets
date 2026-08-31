from django.db import models
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

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    payment_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.booking.booking_code    