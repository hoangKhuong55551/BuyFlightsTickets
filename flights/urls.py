from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("flight/<int:flight_id>/", views.flight_detail, name="flight_detail"),
    path("help/", views.help_center, name="help_center"),
    path("contact/", views.contact_us, name="contact_us"),
    path("boarding-guidelines/", views.boarding_guidelines, name="boarding_guidelines"),
]