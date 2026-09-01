from django.urls import path
from . import views


urlpatterns = [

    path(
        "create/<int:flight_id>/",
        views.create_booking,
        name="create_booking"
    ),

    path(
        "seat/<int:flight_id>/",
        views.seat_selection,
        name="seat_selection"
    ),

    path(
        "passenger/<int:booking_id>/",
        views.passenger,
        name="passenger"
    ),
    path(
    "ticket/<int:booking_id>/",
    views.ticket,
    name="ticket"
    ),
    path(
    "my-bookings/",
    views.my_bookings,
    name="my_bookings"
    ),

    path(
    "cancel/<int:booking_id>/",
    views.cancel_booking,
    name="cancel_booking"
    ),

    path('change-seat/<int:ticket_id>/', views.change_seat, name='change_seat'),
]
