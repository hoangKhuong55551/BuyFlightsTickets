from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("flights.urls")
    ),

    path(
        "users/",
        include("users.urls")
    ),

    path(
        "bookings/",
        include("bookings.urls")
    ),

    path(
        "payments/",
        include("payments.urls")
    ),
    path(
    "recommendations/",
    include("recommendations.urls")
    ),  

]