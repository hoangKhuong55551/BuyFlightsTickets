from django.db import models


class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    logo = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Airport(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Aircraft(models.Model):
    model = models.CharField(max_length=100)
    registration_number = models.CharField(
        max_length=50,
        unique=True
    )
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return self.registration_number


class Flight(models.Model):

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("boarding", "Boarding"),
        ("departed", "Departed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    flight_number = models.CharField(max_length=20)

    airline = models.ForeignKey(
        Airline,
        on_delete=models.CASCADE,
        related_name="flights"
    )

    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.CASCADE,
        related_name="flights"
    )

    departure_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departures"
    )

    arrival_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arrivals"
    )

    departure_time = models.DateTimeField(db_index=True)
    arrival_time = models.DateTimeField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled",
        db_index=True
    )

    def __str__(self):
        return self.flight_number