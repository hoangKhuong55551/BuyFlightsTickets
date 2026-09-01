from django.db import models

class Destination(models.Model):
    BADGE_CHOICES = [
        ("hot", "Hot"),
        ("new", "New"),
        ("deal", "Deal"),
    ]

    name = models.CharField(max_length=100, verbose_name="City/Destination Name")
    country = models.CharField(max_length=100, default="Vietnam", verbose_name="Country")
    airport_code = models.CharField(max_length=10, blank=True, verbose_name="Airport Code")
    image_url = models.URLField(verbose_name="Image URL")
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Starting Price")
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, null=True, verbose_name="Badge")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

    def __str__(self):
        return f"{self.name} ({self.airport_code})"
