from django.contrib import admin
from .models import Airline, Airport, Aircraft, Flight


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    search_fields = ["name", "code"]


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "city"]
    search_fields = ["name", "code", "city"]


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ["registration_number", "model", "total_seats"]
    search_fields = ["registration_number", "model"]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        "flight_number", "airline",
        "departure_airport", "arrival_airport",
        "departure_time", "arrival_time",
        "price", "status"
    ]
    list_filter = ["status", "airline", "departure_airport", "arrival_airport"]
    search_fields = ["flight_number"]
    date_hierarchy = "departure_time"
