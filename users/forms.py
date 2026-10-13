from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.Form):

    first_name = forms.CharField(
        max_length=150,
        label="Họ & tên đệm",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nguyễn Văn"})
    )

    last_name = forms.CharField(
        max_length=150,
        label="Tên",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "An"})
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "example@email.com"})
    )

    phone = forms.CharField(
        max_length=20,
        label="Số điện thoại",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "0912 345 678 (tuỳ chọn)"})
    )

    date_of_birth = forms.DateField(
        label="Ngày / Năm sinh",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    password = forms.CharField(
        label="Mật khẩu",
        min_length=6,
        widget=forms.PasswordInput(attrs={"placeholder": "Tối thiểu 6 ký tự"})
    )

    confirm_password = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={"placeholder": "Nhập lại mật khẩu"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được dùng cho tài khoản khác.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            # Chạy tất cả AUTH_PASSWORD_VALIDATORS đã cấu hình trong settings.py
            validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Mật khẩu xác nhận không khớp.")
        return cleaned_data


class LoginForm(forms.Form):

    login_id = forms.CharField(
        label="Email hoặc Mã định danh (ID)",
        widget=forms.TextInput(attrs={"placeholder": "Nhập email hoặc mã ID (SKB-...)"})
    )

    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={"placeholder": "Mật khẩu"})
    )


class ProfileForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        label="Họ",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Nhập họ"})
    )
    last_name = forms.CharField(
        max_length=150,
        label="Tên",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Nhập tên"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "example@email.com"})
    )
    phone = forms.CharField(
        max_length=20,
        label="Số điện thoại",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "0912 345 678"})
    )
    date_of_birth = forms.DateField(
        label="Ngày sinh",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    national_id = forms.CharField(
        max_length=30,
        label="CCCD / Passport",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Số CCCD hoặc Passport"})
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self.user and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Email này đã được dùng cho tài khoản khác.")
        return email
