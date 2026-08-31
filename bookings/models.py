from django.db import models
from django.contrib.auth.models import User
from flights.models import Flight


class Booking(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        db_index=True
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings"
    )

    booking_code = models.CharField(
        max_length=20,
        unique=True
    )

    booking_date = models.DateTimeField(
        auto_now_add=True
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return self.booking_code


class Passenger(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="passengers"
    )

    full_name = models.CharField(max_length=150)

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    passport_number = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return f"{self.full_name} ({self.booking.booking_code})"


class Ticket(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE
    )

    seat_number = models.CharField(
        max_length=10
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.flight} - {self.seat_number}"