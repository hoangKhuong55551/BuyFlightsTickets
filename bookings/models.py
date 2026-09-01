from django.db import models
from django.contrib.auth.models import User
from flights.models import Flight

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", db_index=True, verbose_name="User")
    
    # Outbound flight
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True, related_name="outbound_bookings", verbose_name="Outbound Flight")
    
    # Return flight (Optional, for round trips)
    return_flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True, related_name="return_bookings", verbose_name="Return Flight")

    booking_code = models.CharField(max_length=20, unique=True, verbose_name="Booking Code")
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Booking Date")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Price")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Status")

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return self.booking_code

class Passenger(models.Model):
    PASSENGER_TYPE_CHOICES = [
        ("adult", "Adult"),
        ("child", "Child"),
        ("infant", "Infant"),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="passengers", verbose_name="Booking")
    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    passport_number = models.CharField(max_length=50, blank=True, verbose_name="Passport Number")
    passenger_type = models.CharField(max_length=10, choices=PASSENGER_TYPE_CHOICES, default="adult", verbose_name="Passenger Type")

    class Meta:
        verbose_name = "Passenger"
        verbose_name_plural = "Passengers"

    def __str__(self):
        return f"{self.full_name} ({self.booking.booking_code})"

class Ticket(models.Model):
    SEAT_CLASS_CHOICES = [
        ("economy", "Economy"),
        ("business", "Business"),
        ("first", "First Class"),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="tickets", verbose_name="Booking")
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, verbose_name="Passenger")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, verbose_name="Flight")
    seat_number = models.CharField(max_length=10, verbose_name="Seat Number")
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS_CHOICES, default="economy", verbose_name="Seat Class")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price")

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        # Ensure each seat on each flight is booked only once
        unique_together = [('flight', 'seat_number')]

    def __str__(self):
        return f"{self.flight} - {self.seat_number} ({self.get_seat_class_display()})"
