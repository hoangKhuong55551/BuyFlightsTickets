from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "flight/<int:flight_id>/",
        views.flight_detail,
        name="flight_detail"
    ),

]