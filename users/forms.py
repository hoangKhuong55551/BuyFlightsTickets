from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={"placeholder": "Nhập tên đăng nhập"})
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

    password = forms.CharField(
        label="Mật khẩu",
        min_length=6,
        widget=forms.PasswordInput(attrs={"placeholder": "Tối thiểu 6 ký tự"})
    )

    confirm_password = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={"placeholder": "Nhập lại mật khẩu"})
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên đăng nhập đã tồn tại.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được dùng cho tài khoản khác.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Mật khẩu xác nhận không khớp.")
        return cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={"placeholder": "Tên đăng nhập"})
    )

    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={"placeholder": "Mật khẩu"})
    )

