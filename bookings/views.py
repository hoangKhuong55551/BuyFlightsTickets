import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PassengerForm
from .models import Booking, Passenger, Ticket
from flights.models import Flight


def _generate_seats(flight):
    """
    Tạo danh sách ghế có cấu trúc theo hàng, phân chia loại ghế và lối thoát hiểm.
    """
    from bookings.models import Ticket
    taken = set(
        Ticket.objects.filter(
            flight=flight,
            booking__status__in=["pending", "paid"]
        ).values_list("seat_number", flat=True)
    )
    total = getattr(getattr(flight, "aircraft", None), "total_seats", 180) # default 180 seats for A320
    seat_letters = ["A", "B", "C", "D", "E", "F"]
    seats_per_row = len(seat_letters)
    total_rows = (total + seats_per_row - 1) // seats_per_row
    
    rows = []
    count = 0
    for row in range(1, total_rows + 1):
        # Determine seat type for coloring
        if row <= 3:
            seat_type = "premium"
        elif row <= 11:
            seat_type = "front"
        else:
            seat_type = "standard"
            
        is_exit = row in [11, 12, 26, 27]
        
        row_seats = []
        for letter in seat_letters:
            if count >= total:
                break
            code = f"{row:02d}{letter}"
            row_seats.append({
                "code": code,
                "letter": letter,
                "taken": code in taken,
            })
            count += 1
            
        rows.append({
            "row_number": row,
            "type": seat_type,
            "is_exit": is_exit,
            "seats": row_seats
        })
        
    return rows


@login_required
@transaction.atomic
def create_booking(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == "POST":
        seat_number = request.POST.get("seat_number", "").strip()

        if not seat_number:
            messages.error(request, "Vui lÃ²ng chá»n gháº¿ trÆ°á»›c khi Ä‘áº·t vÃ©.")
            return redirect("create_booking", flight_id=flight.id)

        # KhoÃ¡ dÃ²ng Ä‘á»ƒ trÃ¡nh race condition â€” hai user chá»n cÃ¹ng gháº¿ Ä‘á»“ng thá»i
        already_taken = (
            Ticket.objects
            .select_for_update()
            .filter(
                flight=flight,
                seat_number=seat_number,
                booking__status__in=["pending", "paid"]
            )
            .exists()
        )
        if already_taken:
            messages.error(
                request,
                f"Gháº¿ {seat_number} vá»«a Ä‘Æ°á»£c ngÆ°á»i khÃ¡c Ä‘áº·t. Vui lÃ²ng chá»n gháº¿ khÃ¡c."
            )
            return redirect("create_booking", flight_id=flight.id)

        booking_code = uuid.uuid4().hex[:10].upper()

        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            booking_code=booking_code,
            total_price=flight.price,
            status="pending"
        )

        request.session["selected_seat"] = seat_number
        return redirect("passenger", booking_id=booking.id)

    all_seats = _generate_seats(flight)
    return render(
        request,
        "bookings/create.html",
        {"flight": flight, "all_seats": all_seats}
    )



@login_required(login_url="/users/login/")
def seat_selection(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    all_seats = _generate_seats(flight)
    return render(
        request,
        "bookings/seat_selection.html",
        {"flight": flight, "all_seats": all_seats}
    )


@login_required(login_url="/users/login/")
def passenger(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            p = Passenger.objects.create(
                booking=booking,
                full_name=form.cleaned_data["full_name"],
                date_of_birth=form.cleaned_data.get("date_of_birth"),
                passport_number=form.cleaned_data.get("passport_number", "")
            )
            seat_number = request.session.pop("selected_seat", "N/A")
            if booking.flight:
                Ticket.objects.create(
                    booking=booking,
                    passenger=p,
                    flight=booking.flight,
                    seat_number=seat_number,
                    price=booking.total_price
                )
            return redirect("payment", booking_id=booking.id)
    else:
        form = PassengerForm()

    return render(
        request,
        "bookings/passenger.html",
        {"booking": booking, "form": form}
    )


@login_required(login_url="/users/login/")
def ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "bookings/ticket.html", {"booking": booking})


@login_required(login_url="/users/login/")
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).select_related("flight").order_by("-booking_date")
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        if booking.status == "pending":
            booking.status = "cancelled"
            booking.save()
            messages.success(request, f"Đã huỷ vé {booking.booking_code}. Ghế đã được giải phóng.")
        else:
            messages.error(request, "Chỉ có thể huỷ vé đang ở trạng thái chờ thanh toán.")
        return redirect("my_bookings")

    return render(request, "bookings/cancel_confirm.html", {"booking": booking})

