from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from django.http import HttpResponseForbidden
from bookings.models import Booking
from flights.models import Flight, Airline
import json

@login_required
def dashboard_home(request):
    user = request.user
    is_airline_manager = hasattr(user, 'profile') and user.profile.managed_airline is not None
    
    if not (user.is_superuser or is_airline_manager):
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")
        
    airline = None
    if is_airline_manager and not user.is_superuser:
        airline = user.profile.managed_airline
        
    # Lấy các booking đã thanh toán
    bookings = Booking.objects.filter(status='paid')
    if airline:
        bookings = bookings.filter(flight__airline=airline)
        
    # 1. Doanh thu theo tháng (6 tháng gần nhất)
    # Rất cơ bản: Gom nhóm theo tháng. Django có TruncMonth nhưng sqlite đôi khi gặp khó.
    # Ta sẽ xử lý bằng python cho nhanh nếu ít data, hoặc dùng sqlite datetime.
    
    # Ta lấy 6 tháng gần nhất
    from dateutil.relativedelta import relativedelta
    now = timezone.now()
    months_labels = []
    revenue_data = []
    for i in range(5, -1, -1):
        m = now - relativedelta(months=i)
        start = m.replace(day=1, hour=0, minute=0, second=0)
        # End of month is start of next month
        end = start + relativedelta(months=1)
        
        m_bookings = bookings.filter(booking_date__gte=start, booking_date__lt=end)
        total = m_bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        months_labels.append(m.strftime('%m/%Y'))
        revenue_data.append(float(total))
        
    # 2. Hãng bay đặt nhiều nhất (Chỉ admin mới cần xem)
    top_airlines_labels = []
    top_airlines_data = []
    if not airline:
        # Lấy top 5 hãng
        top_airlines = Booking.objects.filter(status='paid').values('flight__airline__name').annotate(total=Count('id')).order_by('-total')[:5]
        for item in top_airlines:
            top_airlines_labels.append(item['flight__airline__name'] or 'Khác')
            top_airlines_data.append(item['total'])
            
    # 3. Tuyến bay hot nhất
    top_routes_labels = []
    top_routes_data = []
    
    routes_qs = bookings.values('flight__departure_airport__code', 'flight__arrival_airport__code').annotate(total=Count('id')).order_by('-total')[:5]
    for item in routes_qs:
        route_name = f"{item['flight__departure_airport__code']} - {item['flight__arrival_airport__code']}"
        top_routes_labels.append(route_name)
        top_routes_data.append(item['total'])

    context = {
        'airline': airline,
        'months_labels_json': json.dumps(months_labels),
        'revenue_data_json': json.dumps(revenue_data),
        'top_airlines_labels_json': json.dumps(top_airlines_labels),
        'top_airlines_data_json': json.dumps(top_airlines_data),
        'top_routes_labels_json': json.dumps(top_routes_labels),
        'top_routes_data_json': json.dumps(top_routes_data),
        'total_revenue': sum(revenue_data),
        'total_bookings': bookings.count(),
    }
    return render(request, 'dashboard/index.html', context)
