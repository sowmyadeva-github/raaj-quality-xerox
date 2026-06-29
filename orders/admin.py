from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "customer_name",
        "phone_number",
        "service",
        "copies",
        "print_type",
        "paper_size",
        "status",
        "payment_method",
        "payment_status",
        "total_price",
        "created_at",
    )

    list_editable = (
        "status",
        "payment_status",
    )

    list_filter = (
        "status",
        "payment_method",
        "payment_status",
        "service",
        "print_type",
        "paper_size",
        "created_at",
    )

    search_fields = (
        "order_id",
        "customer_name",
        "phone_number",
    )

    readonly_fields = (
        "order_id",
        "created_at",
        "total_price",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Order Information", {
            "fields": (
                "order_id",
                "service",
                "document",
                "copies",
                "print_type",
                "paper_size",
                "instructions",
            )
        }),
        ("Customer Information", {
            "fields": (
                "customer_name",
                "phone_number",
            )
        }),
        ("Status & Payment", {
            "fields": (
                "status",
                "payment_method",
                "payment_status",
                "total_price",
            )
        }),
        ("Date Information", {
            "fields": (
                "created_at",
            )
        }),
    )