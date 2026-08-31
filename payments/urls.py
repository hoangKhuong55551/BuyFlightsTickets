from django.urls import path
from . import views


urlpatterns = [

    path(
        "<int:booking_id>/",
        views.payment,
        name="payment"
    ),

]