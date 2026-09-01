from django.urls import path
from . import views


urlpatterns = [

    path(
        "<int:booking_id>/",
        views.payment,
        name="payment"
    ),

    path(
        "refund/<int:booking_id>/",
        views.request_refund,
        name="request_refund"
    ),

]