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

    def delete_model(self, request, obj):
        booking = obj.booking
        super().delete_model(request, obj)
        if booking:
            booking.status = "cancelled"
            booking.save(update_fields=["status"])

    def delete_queryset(self, request, queryset):
        # Lưu lại danh sách các booking liên quan trước khi xoá vé
        bookings = [obj.booking for obj in queryset if obj.booking]
        super().delete_queryset(request, queryset)
        for booking in bookings:
            booking.status = "cancelled"
            booking.save(update_fields=["status"])
