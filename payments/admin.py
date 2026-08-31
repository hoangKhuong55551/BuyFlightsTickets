from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["booking", "amount", "method", "status", "payment_date"]
    list_filter = ["status", "method"]
    search_fields = ["booking__booking_code"]
