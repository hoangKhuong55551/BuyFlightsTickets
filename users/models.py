from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
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

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile of {self.user.username}"


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
