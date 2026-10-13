import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def generate_user_id():
    """Generate a unique user ID in the format SKB-XXXXXXXX."""
    return f"SKB-{uuid.uuid4().hex[:8].upper()}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    member_id = models.CharField(
        max_length=12,
        unique=True,
        default=generate_user_id,
        editable=False,
        verbose_name="Mã định danh (User ID)"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Phone Number"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of Birth"
    )
    national_id = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="National ID / Passport"
    )
    avatar = models.URLField(
        blank=True,
        verbose_name="Avatar URL"
    )
    managed_airline = models.ForeignKey(
        'flights.Airline',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Hãng hàng không quản lý (Dành cho Đối tác)",
        related_name="managers"
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.member_id} - {self.user.email}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Subscribed At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Rating (1-5)")
    comment = models.TextField(blank=True, verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        user_display = self.user.profile.member_id if self.user and hasattr(self.user, 'profile') else 'Anonymous'
        return f"Review by {user_display} - {self.rating}*"
