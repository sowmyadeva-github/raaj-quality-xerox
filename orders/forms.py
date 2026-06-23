from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer_name",
            "phone_number",
            "service",
            "document",
            "copies",
            "print_type",
            "paper_size",
            "instructions",
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name"
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }),
            "service": forms.Select(attrs={"class": "form-control"}),
            "document": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "copies": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),
            "print_type": forms.Select(attrs={"class": "form-control"}),
            "paper_size": forms.Select(attrs={"class": "form-control"}),
            "instructions": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Any special instructions"
            }),
        }


class TrackOrderForm(forms.Form):
    order_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Order ID e.g. RQX-219093"
        })
    )

    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter phone number used for order"
        })
    )