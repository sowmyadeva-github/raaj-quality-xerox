from django.db import models
from services.models import Service
import uuid


class Order(models.Model):
    PRINT_TYPE_CHOICES = [
        ("bw", "Black & White"),
        ("color", "Color"),
    ]

    PAPER_SIZE_CHOICES = [
        ("A4", "A4"),
        ("A3", "A3"),
        ("Letter", "Letter"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("printing", "Printing"),
        ("ready", "Ready for Pickup"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("pay_at_shop", "Pay at Shop"),
        ("online", "Online Payment"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    order_id = models.CharField(max_length=30, unique=True, blank=True)
    customer_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="orders")

    document = models.FileField(upload_to="orders/documents/")
    copies = models.PositiveIntegerField(default=1)
    print_type = models.CharField(max_length=20, choices=PRINT_TYPE_CHOICES, default="bw")
    paper_size = models.CharField(max_length=20, choices=PAPER_SIZE_CHOICES, default="A4")

    instructions = models.TextField(blank=True, null=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="pay_at_shop"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.order_id:
            random_part = str(uuid.uuid4().int)[:6]
            self.order_id = f"RQX-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.customer_name}"