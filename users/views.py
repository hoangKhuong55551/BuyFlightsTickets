from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import NewsletterSubscriber


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from NguyenNgocHoangKhuong_CNPM24CT1.utils import send_email_bg

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Tạo user nhưng chưa cho phép đăng nhập
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            user.is_active = False # Khóa tài khoản
            user.save()
            
            # Lưu số điện thoại vào profile
            phone = form.cleaned_data.get("phone", "")
            if phone:
                user.profile.phone = phone
                user.profile.save()

            # Tạo link xác thực
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request).domain
            verify_url = f"http://{current_site}/users/verify/{uid}/{token}/"

            # Render html và gửi email
            html_content = render_to_string("emails/verify_email.html", {
                "user": user,
                "verify_url": verify_url
            })
            send_email_bg(user.email, "SkyBook - Xác thực tài khoản của bạn", html_content)

            messages.success(request, "Đăng ký thành công! Vui lòng kiểm tra email để xác thực tài khoản trước khi đăng nhập.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Tài khoản của bạn đã được xác thực thành công. Bạn có thể đăng nhập ngay!")
        return redirect("login")
    else:
        messages.error(request, "Link xác thực không hợp lệ hoặc đã hết hạn.")
        return redirect("login")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Chào mừng, {user.username}!")
                return redirect("home")
            else:
                # Kiểm tra xem user có tồn tại nhưng bị vô hiệu hóa (is_active=False) không
                username = form.cleaned_data["username"]
                try:
                    u = User.objects.get(username=username)
                    if not u.is_active:
                        messages.error(request, "Tài khoản của bạn chưa được xác thực. Vui lòng kiểm tra email để kích hoạt.")
                    else:
                        messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
                except User.DoesNotExist:
                    messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Bạn đã đăng xuất.")
    return redirect("home")


@login_required
def profile(request):
    """Trang xem/sửa thông tin cá nhân."""
    user = request.user
    user_profile = user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, user=user)
        if form.is_valid():
            # Cập nhật User
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()

            # Cập nhật UserProfile
            user_profile.phone = form.cleaned_data["phone"]
            user_profile.date_of_birth = form.cleaned_data.get("date_of_birth")
            user_profile.national_id = form.cleaned_data.get("national_id", "")
            user_profile.save()

            messages.success(request, "Cập nhật thông tin thành công!")
            return redirect("profile")
    else:
        form = ProfileForm(initial={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user_profile.phone,
            "date_of_birth": user_profile.date_of_birth,
            "national_id": user_profile.national_id,
        }, user=user)

    # Thống kê booking
    from bookings.models import Booking
    total_bookings = Booking.objects.filter(user=user).count()
    paid_bookings = Booking.objects.filter(user=user, status="paid").count()
    cancelled_bookings = Booking.objects.filter(user=user, status="cancelled").count()

    return render(request, "users/profile.html", {
        "form": form,
        "total_bookings": total_bookings,
        "paid_bookings": paid_bookings,
        "cancelled_bookings": cancelled_bookings,
    })


def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if not email:
            return JsonResponse({"success": False, "message": "Vui lòng nhập địa chỉ email."})
        try:
            NewsletterSubscriber.objects.create(email=email)
            return JsonResponse({"success": True, "message": "Đăng ký thành công! Cảm ơn bạn."})
        except Exception:
            return JsonResponse({"success": False, "message": "Email này đã đăng ký nhận tin rồi!"})
    return JsonResponse({"success": False, "message": "Phương thức không hợp lệ."})

