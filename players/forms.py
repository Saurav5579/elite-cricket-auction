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

    # =========================
    # PHOTO VALIDATION
    # =========================
    def clean_photo(self):

        photo = self.cleaned_data.get("photo")

        if not photo:
            raise forms.ValidationError("Photo is required")

        # JPG check
        if not photo.name.lower().endswith((".jpg", ".jpeg")):
            raise forms.ValidationError("Photo must be JPG format")

        # Size check (10KB - 20KB)
        if photo.size < 10000 or photo.size > 20000:
            raise forms.ValidationError("Photo size must be between 10KB and 20KB")

        return photo

# =========================
# DOCUMENT VALIDATION
# =========================
def clean_document(self):

    document = self.cleaned_data.get("document")

    if not document:
        raise forms.ValidationError("Document is required")

    # Allowed formats
    if not document.name.lower().endswith((".pdf", ".jpg", ".jpeg")):
        raise forms.ValidationError("Document must be PDF or JPG format")

    # Size check (50KB - 500KB)
    if document.size < 50000 or document.size > 500000:
        raise forms.ValidationError("Document size must be between 50KB and 500KB")

    return document

    # =========================
    # DUPLICATE MOBILE CHECK
    # =========================
    def clean_mobile(self):

        mobile = self.cleaned_data.get("mobile")

        if Player.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This mobile number is already registered")

        return mobile


    # =========================
    # DUPLICATE EMAIL CHECK
    # =========================
    def clean_email(self):

        email = self.cleaned_data.get("email")

        if Player.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")

        return email