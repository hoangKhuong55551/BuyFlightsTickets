from django import forms


class PassengerForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        label="Họ và tên",
        widget=forms.TextInput(attrs={"placeholder": "Nguyen Van A"})
    )
    
    date_of_birth = forms.DateField(
        label="Ngày sinh",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    passport_number = forms.CharField(
        max_length=50,
        label="CCCD / Passport",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nhập số CCCD/Passport"})
    )
    
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "email@example.com"})
    )
    
    phone_number = forms.CharField(
        max_length=20,
        label="Số điện thoại",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "0901234567"})
    )

