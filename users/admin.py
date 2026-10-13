from django import forms
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from .models import UserProfile, NewsletterSubscriber


class CustomAdminAuthenticationForm(AdminAuthenticationForm):
    username = forms.CharField(
        label="Email / Mã ID / Username",
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "placeholder": "Email, Mã ID (SKB-...) hoặc Username"
        }),
    )


admin.site.login_form = CustomAdminAuthenticationForm

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["member_id", "user", "get_email", "phone", "date_of_birth"]
    search_fields = ["member_id", "user__email", "phone"]
    readonly_fields = ["member_id"]

    @admin.display(description="Email")
    def get_email(self, obj):
        return obj.user.email

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
from NguyenNgocHoangKhuong_CNPM24CT1.utils import send_email_bg

# Hủy đăng ký User mặc định
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Thêm cột user_id vào danh sách hiển thị
    list_display = ('get_user_id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active_display')
    
    # Cho phép lọc theo trạng thái xác thực
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    
    # Tìm kiếm theo email và member_id
    search_fields = ('email', 'profile__member_id', 'first_name', 'last_name')
    
    # Đăng ký các action thủ công
    actions = ['action_verify_users', 'action_resend_verification']

    @admin.display(description="Mã định danh (ID)")
    def get_user_id(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.member_id
        return '-'

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
