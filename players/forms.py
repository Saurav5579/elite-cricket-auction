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
            "name": forms.TextInput(attrs={
                "placeholder": "Enter full name",
                "class": "form-control",
                "required": True
            }),

            "age": forms.NumberInput(attrs={
                "placeholder": "Enter age",
                "class": "form-control",
                "required": True
            }),

            "city": forms.TextInput(attrs={
                "placeholder": "Enter city",
                "class": "form-control",
                "required": True
            }),

            "mobile": forms.TextInput(attrs={
                "placeholder": "Enter mobile number",
                "class": "form-control",
                "required": True
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "Enter email address",
                "class": "form-control",
                "required": True
            }),
        }

    # =========================
    # MOBILE VALIDATION
    # =========================
    def clean_mobile(self):

        mobile = self.cleaned_data.get("mobile")

        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10 digit mobile number")

        if Player.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This mobile number is already registered")

        return mobile


    # =========================
    # EMAIL VALIDATION
    # =========================
    def clean_email(self):

        email = self.cleaned_data.get("email")

        if Player.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")

        return email


    # =========================
# PHOTO VALIDATION
# =========================
def clean_photo(self):

    photo = self.cleaned_data.get("photo")

    if not photo:
        raise forms.ValidationError("Photo is required")

    # ✅ Allow all image formats
    if not photo.name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        raise forms.ValidationError("Only JPG, JPEG, PNG, WEBP images are allowed")

    # ✅ Max size 5MB
    if photo.size > 5 * 1024 * 1024:
        raise forms.ValidationError("Photo size must be less than 5MB")

    return photo


# =========================
# DOCUMENT VALIDATION
# =========================
def clean_document(self):

    document = self.cleaned_data.get("document")

    if not document:
        raise forms.ValidationError("Document is required")

    # ✅ Allow more formats
    if not document.name.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
        raise forms.ValidationError("Document must be PDF, JPG, JPEG or PNG")

    # ✅ Max size 10MB
    if document.size > 10 * 1024 * 1024:
        raise forms.ValidationError("Document size must be less than 10MB")

    return document