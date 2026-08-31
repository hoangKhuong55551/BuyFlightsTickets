from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        label="Ten dang nhap",
        widget=forms.TextInput(attrs={"placeholder": "Nhap ten dang nhap"})
    )

    password = forms.CharField(
        label="Mat khau",
        min_length=6,
        widget=forms.PasswordInput(attrs={"placeholder": "Toi thieu 6 ky tu"})
    )

    confirm_password = forms.CharField(
        label="Xac nhan mat khau",
        widget=forms.PasswordInput(attrs={"placeholder": "Nhap lai mat khau"})
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ten dang nhap da ton tai.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Mat khau xac nhan khong khop.")
        return cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        label="Ten dang nhap",
        widget=forms.TextInput(attrs={"placeholder": "Ten dang nhap"})
    )

    password = forms.CharField(
        label="Mat khau",
        widget=forms.PasswordInput(attrs={"placeholder": "Mat khau"})
    )
