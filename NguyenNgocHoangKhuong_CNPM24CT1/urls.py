from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    path("dashboard/", include("dashboard.urls")),
    path(
        "admin/",
        admin.site.urls
    ),

    path("dashboard/", include("dashboard.urls")),
    path(
        "",
        include("flights.urls")
    ),

    path("dashboard/", include("dashboard.urls")),
    path(
        "users/",
        include("users.urls")
    ),

    path("dashboard/", include("dashboard.urls")),
    path(
        "bookings/",
        include("bookings.urls")
    ),

    path("dashboard/", include("dashboard.urls")),
    path(
        "accounts/",
        include("allauth.urls")
    ),

    path("dashboard/", include("dashboard.urls")),
    path(
        "payments/",
        include("payments.urls")
    ),
    path("dashboard/", include("dashboard.urls")),
    path(
    "recommendations/",
    include("recommendations.urls")
    ),  

]