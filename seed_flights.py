import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from flights.models import Flight, Airline, Airport, Aircraft
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta

# Update existing flights with new fields
for f in Flight.objects.all():
    f.stops = 0
    f.has_checked_baggage = random.choice([True, False])
    f.available_seats = random.randint(5, 180)
    f.save()

# Check if we have enough test airlines
airlines = list(Airline.objects.all())
print(f"Found {len(airlines)} airlines")

# Add more sample airlines if needed
airline_data = [
    {"name": "Vietnam Airlines", "code": "VN", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0e/Vietnam_Airlines_logo.svg/150px-Vietnam_Airlines_logo.svg.png"},
    {"name": "VietJet Air", "code": "VJ", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/VietJet_Air_logo.svg/150px-VietJet_Air_logo.svg.png"},
    {"name": "Bamboo Airways", "code": "QH", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Bamboo_Airways_logo.svg/150px-Bamboo_Airways_logo.svg.png"},
    {"name": "Vietravel Airlines", "code": "VU", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Vietravel_Airlines_logo.svg/150px-Vietravel_Airlines_logo.svg.png"},
    {"name": "Pacific Airlines", "code": "BL", "logo": ""},
]

for a in airline_data:
    airline, created = Airline.objects.get_or_create(code=a["code"], defaults={"name": a["name"], "logo": a["logo"]})
    if created:
        print(f"Created airline: {airline.name}")
    elif airline.logo != a["logo"]:
        airline.logo = a["logo"]
        airline.save()

# Get or create airports
airport_data = [
    {"name": "Sân bay Quốc tế Nội Bài", "code": "HAN", "city": "Hà Nội"},
    {"name": "Sân bay Quốc tế Đà Nẵng", "code": "DAD", "city": "Đà Nẵng"},
    {"name": "Sân bay Quốc tế Tân Sơn Nhất", "code": "SGN", "city": "TP. Hồ Chí Minh"},
    {"name": "Sân bay Quốc tế Phú Quốc", "code": "PQC", "city": "Phú Quốc"},
    {"name": "Sân bay Quốc tế Cam Ranh", "code": "CXR", "city": "Nha Trang"},
    {"name": "Sân bay Liên Khương", "code": "DLI", "city": "Đà Lạt"},
    {"name": "Sân bay Phù Cát", "code": "UIH", "city": "Quy Nhơn"},
    {"name": "Sân bay Vinh", "code": "VII", "city": "Vinh"},
]
for ap in airport_data:
    airport, created = Airport.objects.get_or_create(code=ap["code"], defaults={"name": ap["name"], "city": ap["city"]})
    if created:
        print(f"Created airport: {airport.city}")

# Get or create aircraft
aircraft, _ = Aircraft.objects.get_or_create(
    registration_number="VN-A321-01",
    defaults={"model": "Airbus A321", "total_seats": 180}
)
aircraft2, _ = Aircraft.objects.get_or_create(
    registration_number="VN-A320-02",
    defaults={"model": "Airbus A320", "total_seats": 160}
)

airlines = list(Airline.objects.all())
airports = list(Airport.objects.all())

# Popular routes
routes = [
    ("HAN", "DAD"), ("DAD", "HAN"),
    ("HAN", "SGN"), ("SGN", "HAN"),
    ("HAN", "PQC"), ("SGN", "DAD"),
    ("DAD", "SGN"), ("HAN", "CXR"),
    ("SGN", "PQC"), ("HAN", "DLI"),
]

def get_airport(code):
    return Airport.objects.get(code=code)

base_now = timezone.now().replace(hour=6, minute=0, second=0, microsecond=0)

stops_options = [0, 0, 0, 1, 1, 2]  # Mostly direct
baggage_options = [True, True, False, False, False]

# Generate flights for next 7 days
flights_created = 0
for day_offset in range(0, 7):
    day = base_now + timedelta(days=day_offset)
    for dep_code, arr_code in routes:
        for airline in airlines:
            # Skip some combinations randomly to not have too many
            if random.random() > 0.6:
                continue
            
            dep_hour = random.choice([6, 8, 10, 12, 14, 16, 18, 20, 22])
            dep_time = day.replace(hour=dep_hour, minute=random.choice([0, 15, 30, 45]))
            duration_minutes = random.randint(65, 200)
            arr_time = dep_time + timedelta(minutes=duration_minutes)
            
            base_price = random.randint(800000, 3000000)
            num_stops = random.choice(stops_options)
            has_bag = random.choice(baggage_options)
            seats = random.randint(5, 180)
            
            flight_num = f"{airline.code}{random.randint(100, 999)}"
            ac = aircraft if random.random() > 0.5 else aircraft2
            
            Flight.objects.create(
                flight_number=flight_num,
                airline=airline,
                aircraft=ac,
                departure_airport=get_airport(dep_code),
                arrival_airport=get_airport(arr_code),
                departure_time=dep_time,
                arrival_time=arr_time,
                price=Decimal(base_price),
                status="scheduled",
                stops=num_stops,
                has_checked_baggage=has_bag,
                available_seats=seats
            )
            flights_created += 1

print(f"Created {flights_created} new flights. Total: {Flight.objects.count()}")
