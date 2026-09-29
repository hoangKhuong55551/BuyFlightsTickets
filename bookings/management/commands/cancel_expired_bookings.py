from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import F
from datetime import timedelta

from bookings.models import Booking
from flights.models import Flight


class Command(BaseCommand):
    help = "Tự động huỷ các booking 'pending' đã quá 30 phút và giải phóng ghế."

    def add_arguments(self, parser):
        parser.add_argument(
            "--minutes",
            type=int,
            default=30,
            help="Số phút tối đa cho booking pending (mặc định: 30)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Chỉ hiển thị, không thực sự huỷ",
        )

    def handle(self, *args, **options):
        minutes = options["minutes"]
        dry_run = options["dry_run"]
        expiry = timezone.now() - timedelta(minutes=minutes)

        expired_bookings = Booking.objects.filter(
            status="pending",
            booking_date__lt=expiry
        ).select_related("flight")

        count = expired_bookings.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS("Không có booking pending hết hạn."))
            return

        if dry_run:
            self.stdout.write(self.style.WARNING(
                f"[DRY RUN] Sẽ huỷ {count} booking pending:"
            ))
            for b in expired_bookings:
                self.stdout.write(f"  - {b.booking_code} (tạo lúc {b.booking_date})")
            return

        for booking in expired_bookings:
            # Giải phóng ghế
            ticket_count = booking.tickets.count()
            if ticket_count > 0 and booking.flight:
                Flight.objects.filter(id=booking.flight.id).update(
                    available_seats=F("available_seats") + ticket_count
                )
            booking.tickets.all().delete()

            # Huỷ booking
            booking.status = "cancelled"
            booking.save(update_fields=["status"])

        self.stdout.write(self.style.SUCCESS(
            f"Đã huỷ {count} booking pending hết hạn và giải phóng ghế."
        ))
