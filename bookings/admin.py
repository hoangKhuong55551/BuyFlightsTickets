from django.contrib import admin
from .models import Booking, Passenger, Ticket


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["booking_code", "user", "flight", "total_price", "status", "booking_date"]
    list_filter = ["status"]
    search_fields = ["booking_code", "user__username"]
    date_hierarchy = "booking_date"


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ["full_name", "booking", "passport_number"]
    search_fields = ["full_name", "passport_number", "booking__booking_code"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["booking", "passenger", "flight", "seat_number", "price"]
    search_fields = ["booking__booking_code", "seat_number"]
