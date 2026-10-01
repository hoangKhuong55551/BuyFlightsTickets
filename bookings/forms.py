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
        min_length=10,
        label="CCCD / Passport",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nhập số CCCD/Passport"}),
        error_messages={
            "min_length": "Số CCCD/Passport phải có ít nhất 10 ký tự."
        }
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

    def clean_passport_number(self):
        passport = self.cleaned_data.get('passport_number', '')
        if len(passport) < 10:
            raise forms.ValidationError("CCCD/Passport phải có từ 10 ký tự trở lên.")
        return passport

