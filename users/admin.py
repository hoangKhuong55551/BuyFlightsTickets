from django.contrib import admin
from .models import UserProfile, NewsletterSubscriber

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "date_of_birth"]
    search_fields = ["user__username", "phone"]

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "subscribed_at", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["email"]