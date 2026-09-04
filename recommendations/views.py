from django.shortcuts import render
from django.utils import timezone
from django.db.models import Min, Count
from flights.models import Flight, Airline


def recommendations(request):
    # Base queryset
    base_qs = Flight.objects.select_related(
        "airline", "departure_airport", "arrival_airport"
    ).filter(
        departure_time__gte=timezone.now(),
        status="scheduled"
    )

    # --- Search params from home form ---
    departure = request.GET.get("departure", "").strip()
    arrival = request.GET.get("arrival", "").strip()
    date = request.GET.get("date", "").strip()

    if departure:
        base_qs = base_qs.filter(departure_airport__city__icontains=departure)
    if arrival:
        base_qs = base_qs.filter(arrival_airport__city__icontains=arrival)
    if date:
        base_qs = base_qs.filter(departure_time__date=date)

    # --- Sidebar filter params ---
    filter_stops = request.GET.getlist("stops")       # ["0","1","2"]
    filter_airlines = request.GET.getlist("airline")  # ["VN","VJ"]
    filter_baggage = request.GET.get("has_baggage")   # "1" or ""
    sort_by = request.GET.get("sort", "price")        # price | duration | airline

    filtered_qs = base_qs

    if filter_stops:
        stop_ints = []
        for s in filter_stops:
            if s == "2":
                stop_ints.extend([2, 3, 4, 5])
            else:
                try:
                    stop_ints.append(int(s))
                except ValueError:
                    pass
        filtered_qs = filtered_qs.filter(stops__in=stop_ints)

    if filter_airlines:
        filtered_qs = filtered_qs.filter(airline__code__in=filter_airlines)

    if filter_baggage == "1":
        filtered_qs = filtered_qs.filter(has_checked_baggage=True)

    # Sort
    if sort_by == "duration":
        filtered_qs = filtered_qs.extra(
            select={"duration": "arrival_time - departure_time"}
        ).order_by("duration")
    elif sort_by == "airline":
        filtered_qs = filtered_qs.order_by("airline__name", "price")
    else:
        filtered_qs = filtered_qs.order_by("price")

    # --- Sidebar aggregations (from base_qs before filter) ---
    # Min price for direct flights
    direct_min = base_qs.filter(stops=0).aggregate(m=Min("price"))["m"]
    one_stop_min = base_qs.filter(stops=1).aggregate(m=Min("price"))["m"]
    multi_stop_min = base_qs.filter(stops__gte=2).aggregate(m=Min("price"))["m"]
    baggage_min = base_qs.filter(has_checked_baggage=True).aggregate(m=Min("price"))["m"]
    no_baggage_min = base_qs.filter(has_checked_baggage=False).aggregate(m=Min("price"))["m"]

    # Airlines with min prices (from base_qs)
    airline_prices = (
        base_qs.values("airline__code", "airline__name", "airline__logo")
        .annotate(min_price=Min("price"))
        .order_by("min_price")
    )

    context = {
        "flights": filtered_qs[:50],
        "total_count": filtered_qs.count(),
        "departure": departure,
        "arrival": arrival,
        "date": date,
        # Filter state
        "filter_stops": filter_stops,
        "filter_airlines": filter_airlines,
        "filter_baggage": filter_baggage,
        "sort_by": sort_by,
        # Sidebar data
        "direct_min": direct_min,
        "one_stop_min": one_stop_min,
        "multi_stop_min": multi_stop_min,
        "baggage_min": baggage_min,
        "no_baggage_min": no_baggage_min,
        "airline_prices": airline_prices,
    }

    return render(request, "recommendations/recommendations.html", context)