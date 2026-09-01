from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Payment, RefundRequest

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["booking", "amount", "method", "status", "payment_date"]
    list_filter = ["status", "method"]
    search_fields = ["booking__booking_code"]

class RefundRequestInline(admin.StackedInline):
    model = RefundRequest
    extra = 0
    readonly_fields = ["requested_at", "processed_at", "refund_amount", "status"]
    fields = ["status", "refund_amount", "reason", "admin_note", "requested_at", "processed_at"]
    can_delete = False

@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = [
        "booking_code_link", "user_display", "refund_amount_display",
        "status_badge", "requested_at", "processed_at"
    ]
    list_filter = ["status", "requested_at"]
    search_fields = ["booking__booking_code", "booking__user__username"]
    readonly_fields = ["booking", "requested_at", "processed_at", "refund_amount"]
    fields = [
        "booking", "status", "refund_amount", "reason",
        "admin_note", "requested_at", "processed_at"
    ]
    actions = ["action_approve", "action_reject"]
    ordering = ["-requested_at"]

    @admin.display(description="Mã booking")
    def booking_code_link(self, obj):
        return format_html(
            '<strong style="font-family:monospace;letter-spacing:.05em">{}</strong>',
            obj.booking.booking_code
        )

    @admin.display(description="Hành khách")
    def user_display(self, obj):
        u = obj.booking.user
        return f"{u.get_full_name() or u.username} ({u.email or '-'})"

    @admin.display(description="Số tiền hoàn")
    def refund_amount_display(self, obj):
        amount_str = f"{obj.refund_amount:,.0f}" if obj.refund_amount else "0"
        return format_html(
            '<span style="font-weight:700;color:#1565c0">{} đ</span>',
            amount_str
        )

    @admin.display(description="Trạng thái")
    def status_badge(self, obj):
        colors = {
            "pending":  ("#92400e", "#fef3c7"),
            "approved": ("#065f46", "#d1fae5"),
            "rejected": ("#991b1b", "#fee2e2"),
        }
        fg, bg = colors.get(obj.status, ("#374151", "#f3f4f6"))
        
        status_vn = {
            "pending": "Chờ duyệt",
            "approved": "Đã hoàn tiền",
            "rejected": "Từ chối"
        }
        display_status = status_vn.get(obj.status, obj.status)

        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:99px;'
            'font-size:.78rem;font-weight:700">{}</span>',
            bg, fg, display_status
        )

    @admin.action(description="Duyệt hoàn tiền (Approve)")
    def action_approve(self, request, queryset):
        approved = 0
        skipped = 0
        for refund in queryset.filter(status="pending"):
            refund.approve()
            approved += 1
        skipped = queryset.exclude(status="pending").count()

        if approved:
            self.message_user(
                request,
                f"Đã duyệt {approved} yêu cầu hoàn tiền.",
                level="SUCCESS"
            )
        if skipped:
            self.message_user(
                request,
                f"{skipped} yêu cầu bị bỏ qua.",
                level="WARNING"
            )

    @admin.action(description="Từ chối hoàn tiền (Reject)")
    def action_reject(self, request, queryset):
        rejected = 0
        for refund in queryset.filter(status="pending"):
            refund.reject(note="Từ chối bởi admin.")
            rejected += 1
        if rejected:
            self.message_user(
                request,
                f"Đã từ chối {rejected} yêu cầu hoàn tiền.",
                level="WARNING"
            )