from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "phone_number",
        ]

        widgets = {
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Phone Number",
                }
            ),
        }