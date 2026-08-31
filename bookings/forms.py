from django import forms


class PassengerForm(forms.Form):

    full_name = forms.CharField(
        max_length=150,
        label="Ho va ten",
        widget=forms.TextInput(attrs={"placeholder": "Nguyen Van A"})
    )

    date_of_birth = forms.DateField(
        label="Ngay sinh",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    passport_number = forms.CharField(
        max_length=50,
        label="CCCD / Passport",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Nhap so CCCD hoac Passport"})
    )
