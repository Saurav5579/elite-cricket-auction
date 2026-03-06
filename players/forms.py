from django import forms
from .models import Player


class PlayerForm(forms.ModelForm):

    agreed_terms = forms.BooleanField(
        required=True,
        label="I agree to Auction Rules & Terms"
    )

    class Meta:
        model = Player
        fields = [
            "name",
            "age",
            "city",
            "mobile",
            "email",
            "role",
            "playing_style",
            "experience",
            "base_price",
            "photo",
            "document",
            "agreed_terms",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter full name"}),
            "age": forms.NumberInput(attrs={"placeholder": "Enter age"}),
            "city": forms.TextInput(attrs={"placeholder": "Enter city"}),
            "mobile": forms.TextInput(attrs={"placeholder": "Enter mobile number"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter email address"}),
        }