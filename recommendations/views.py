from django.shortcuts import render
from django.utils import timezone
from flights.models import Flight


def recommendations(request):
    flights = Flight.objects.select_related(
        "airline", "departure_airport", "arrival_airport"
    ).filter(departure_time__gte=timezone.now()).order_by("price")

    return render(
        request,
        "recommendations/recommendations.html",
        {"flights": flights}
    )