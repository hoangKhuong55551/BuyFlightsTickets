from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Flight


def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    return render(
        request,
        "flights/flight_detail.html",
        {"flight": flight}
    )


from bookings.models import Passenger
from users.models import Review
from django.db.models import Avg

def home(request):
    flights = Flight.objects.select_related(
        "airline", "departure_airport", "arrival_airport"
    ).filter(departure_time__gte=timezone.now())

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

    # Real data metrics
    passenger_count = Passenger.objects.count()
    route_count = Flight.objects.values('departure_airport', 'arrival_airport').distinct().count()
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']
    if avg_rating is None:
        avg_rating = 4.9
    else:
        avg_rating = round(avg_rating, 1)

    return render(
        request,
        "home.html",
        {
            "page_obj": page_obj,
            "flights": page_obj,
            "departure": departure,
            "arrival": arrival,
            "date": date,
            "passenger_count": passenger_count,
            "route_count": route_count,
            "avg_rating": avg_rating,
        }
    )


def help_center(request):
    return render(request, 'flights/help_center.html')

def contact_us(request):
    return render(request, 'flights/contact_us.html')

def boarding_guidelines(request):
    return render(request, 'flights/boarding_guidelines.html')