from django.shortcuts import render
from django.utils import timezone
from django.db.models import Min
from flights.models import Flight, Airline


def recommendations(request):
    # Base queryset cho chuyến đi
    base_qs = Flight.objects.select_related(
        "airline", "departure_airport", "arrival_airport"
    ).filter(
        departure_time__gte=timezone.now(),
        status="scheduled"
    )

    # --- Search params từ form ---
    departure = request.GET.get("departure", "").strip()
    arrival = request.GET.get("arrival", "").strip()
    date = request.GET.get("date", "").strip()
    return_date = request.GET.get("return_date", "").strip()
    trip_type = request.GET.get("trip_type", "one_way")  # "round" | "one_way"
    passengers = request.GET.get("passengers", "1").strip()
    seat_class = request.GET.get("seat_class", "economy").strip()

    if departure:
        base_qs = base_qs.filter(departure_airport__city__icontains=departure)
    if arrival:
        base_qs = base_qs.filter(arrival_airport__city__icontains=arrival)
    if date:
        base_qs = base_qs.filter(departure_time__date=date)

    # --- Sidebar filter params ---
    filter_stops = request.GET.getlist("stops")
    filter_airlines = request.GET.getlist("airline")
    filter_baggage = request.GET.get("has_baggage")
    sort_by = request.GET.get("sort", "price")

    # Compute stop_ints once (used for both outbound and return)
    stop_ints = []
    if filter_stops:
        for s in filter_stops:
            if s == "2":
                stop_ints.extend([2, 3, 4, 5])
            else:
                try:
                    stop_ints.append(int(s))
                except ValueError:
                    pass

    def apply_filters(qs):
        if stop_ints:
            qs = qs.filter(stops__in=stop_ints)
        if filter_airlines:
            qs = qs.filter(airline__code__in=filter_airlines)
        if filter_baggage == "1":
            qs = qs.filter(has_checked_baggage=True)
        return qs

    def apply_sort(qs):
        if sort_by == "duration":
            return qs.extra(
                select={"duration": "arrival_time - departure_time"}
            ).order_by("duration")
        elif sort_by == "airline":
            return qs.order_by("airline__name", "price")
        else:
            return qs.order_by("price")

    filtered_qs = apply_sort(apply_filters(base_qs))

    # --- Sidebar aggregations ---
    direct_min = base_qs.filter(stops=0).aggregate(m=Min("price"))["m"]
    one_stop_min = base_qs.filter(stops=1).aggregate(m=Min("price"))["m"]
    multi_stop_min = base_qs.filter(stops__gte=2).aggregate(m=Min("price"))["m"]
    baggage_min = base_qs.filter(has_checked_baggage=True).aggregate(m=Min("price"))["m"]
    no_baggage_min = base_qs.filter(has_checked_baggage=False).aggregate(m=Min("price"))["m"]

    airline_prices = (
        base_qs.values("airline__code", "airline__name", "airline__logo")
        .annotate(min_price=Min("price"))
        .order_by("min_price")
    )

    # --- Chuyến về (Round-trip) ---
    return_flights = None
    return_total_count = 0
    if trip_type == "round" and return_date and departure and arrival:
        return_base = Flight.objects.select_related(
            "airline", "departure_airport", "arrival_airport"
        ).filter(
            departure_time__gte=timezone.now(),
            status="scheduled",
            # Chiều ngược lại
            departure_airport__city__icontains=arrival,
            arrival_airport__city__icontains=departure,
            departure_time__date=return_date,
        )
        return_base = apply_filters(return_base)
        return_total_count = return_base.count()
        return_flights = apply_sort(return_base)[:50]

    context = {
        "flights": filtered_qs[:50],
        "total_count": filtered_qs.count(),
        "departure": departure,
        "arrival": arrival,
        "date": date,
        "return_date": return_date,
        "trip_type": trip_type,
        "passengers": passengers,
        "seat_class": seat_class,
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
        # Round-trip
        "return_flights": return_flights,
        "return_total_count": return_total_count,
        "trip_type": trip_type,
    }

    return render(request, "recommendations/recommendations.html", context)