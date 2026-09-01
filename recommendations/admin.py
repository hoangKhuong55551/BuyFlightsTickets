from django.contrib import admin
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ["name", "airport_code", "country", "starting_price", "badge", "is_active"]
    list_filter = ["is_active", "badge"]
    search_fields = ["name", "airport_code", "country"]