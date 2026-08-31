from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Flight


def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    return render(
        request,
        "flights/flight_detail.html",
        {"flight": flight}
    )


def home(request):
    flights = Flight.objects.select_related(
        "airline", "departure_airport", "arrival_airport"
    ).all()

    departure = request.GET.get("departure", "").strip()
    arrival = request.GET.get("arrival", "").strip()
    date = request.GET.get("date", "").strip()

    if departure:
        flights = flights.filter(departure_airport__city__icontains=departure)

    if arrival:
        flights = flights.filter(arrival_airport__city__icontains=arrival)

    if date:
        flights = flights.filter(departure_time__date=date)

    paginator = Paginator(flights, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home.html",
        {
            "page_obj": page_obj,
            "flights": page_obj,
            "departure": departure,
            "arrival": arrival,
            "date": date,
        }
    )
