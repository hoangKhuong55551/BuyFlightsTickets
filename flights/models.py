from django.db import models

class Airline(models.Model):
    name = models.CharField(max_length=100, verbose_name="Airline Name")
    code = models.CharField(max_length=10, unique=True, verbose_name="Airline Code")
    logo = models.URLField(blank=True, verbose_name="Logo URL")

    class Meta:
        verbose_name = "Airline"
        verbose_name_plural = "Airlines"

    def __str__(self):
        return f"{self.name} ({self.code})"

class Airport(models.Model):
    name = models.CharField(max_length=150, verbose_name="Airport Name")
    code = models.CharField(max_length=10, unique=True, verbose_name="Airport Code")
    city = models.CharField(max_length=100, verbose_name="City")

    class Meta:
        verbose_name = "Airport"
        verbose_name_plural = "Airports"

    def __str__(self):
        return f"{self.name} ({self.code})"

class Aircraft(models.Model):
    model = models.CharField(max_length=100, verbose_name="Aircraft Model")
    registration_number = models.CharField(max_length=50, unique=True, verbose_name="Registration Number")
    total_seats = models.PositiveIntegerField(verbose_name="Total Seats")

    class Meta:
        verbose_name = "Aircraft"
        verbose_name_plural = "Aircrafts"

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

    flight_number = models.CharField(max_length=20, verbose_name="Flight Number")
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name="flights", verbose_name="Airline")
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="flights", verbose_name="Aircraft")
    
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures", verbose_name="Departure Airport")
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals", verbose_name="Arrival Airport")
    
    departure_time = models.DateTimeField(db_index=True, verbose_name="Departure Time")
    arrival_time = models.DateTimeField(verbose_name="Arrival Time")
    
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Base Price")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled", db_index=True, verbose_name="Status")

    class Meta:
        verbose_name = "Flight"
        verbose_name_plural = "Flights"

    def __str__(self):
        return self.flight_number
