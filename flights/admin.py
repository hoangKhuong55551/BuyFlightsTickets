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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile') and request.user.profile.managed_airline:
            return qs.filter(airline=request.user.profile.managed_airline)
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.managed_airline:
            if db_field.name == "airline":
                kwargs["queryset"] = Airline.objects.filter(id=request.user.profile.managed_airline.id)
                kwargs["initial"] = request.user.profile.managed_airline.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.managed_airline:
            obj.airline = request.user.profile.managed_airline
        super().save_model(request, obj, form, change)
