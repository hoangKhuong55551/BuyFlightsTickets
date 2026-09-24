from django.contrib import admin
from .models import UserProfile, NewsletterSubscriber

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "date_of_birth"]
    search_fields = ["user__username", "phone"]

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "subscribed_at", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["email"]

# --- TÙY CHỈNH ADMIN CHO USER (ĐỂ QUẢN LÝ XÁC THỰC EMAIL) ---
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from config.utils import send_email_bg

# Hủy đăng ký User mặc định
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Thêm cột is_active vào danh sách hiển thị
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active_display')
    
    # Cho phép lọc theo trạng thái xác thực
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    
    # Đăng ký các action thủ công
    actions = ['action_verify_users', 'action_resend_verification']

    @admin.display(boolean=True, description="Đã xác thực (Active)")
    def is_active_display(self, obj):
        return obj.is_active

    @admin.action(description="Bỏ qua bảo mật: Xác thực thủ công các tài khoản đã chọn")
    def action_verify_users(self, request, queryset):
        count = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, f"Đã kích hoạt thủ công thành công {count} tài khoản.")

    @admin.action(description="Gửi lại Email xác thực cho các tài khoản chưa active")
    def action_resend_verification(self, request, queryset):
        unverified_users = queryset.filter(is_active=False)
        count = 0
        current_site = get_current_site(request).domain
        
        for user in unverified_users:
            if user.email:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                verify_url = f"http://{current_site}/users/verify/{uid}/{token}/"
                
                html_content = render_to_string("emails/verify_email.html", {
                    "user": user,
                    "verify_url": verify_url
                })
                send_email_bg(user.email, "SkyBook - Xác thực tài khoản của bạn", html_content)
                count += 1
                
        self.message_user(request, f"Đã gửi lại link xác thực cho {count} người dùng.")