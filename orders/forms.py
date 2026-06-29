from django import forms
from .models import Order


ALLOWED_FILE_EXTENSIONS = [
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".jpg",
    ".jpeg",
    ".png",
]


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
            "payment_method",
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
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            "instructions": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Any special instructions"
            }),
        }

    def clean_document(self):
        document = self.cleaned_data.get("document")

        if document:
            file_name = document.name.lower()
            if not any(file_name.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS):
                raise forms.ValidationError(
                    "Unsupported file type. Please upload PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX, JPG, JPEG, or PNG files only."
                )

        return document


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