from django.shortcuts import render
from flights.models import Flight


def recommendations(request):
    flights = Flight.objects.select_related(
        "airline", "departure_airport", "arrival_airport"
    ).order_by("price")

    return render(
        request,
        "recommendations/recommendations.html",
        {"flights": flights}
    )
