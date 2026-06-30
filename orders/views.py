from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm, TrackOrderForm
from .models import Order


def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)

            service_price = order.service.base_price
            total = service_price * order.copies

            if order.print_type == "color":
                total += 5 * order.copies

            order.total_price = total
            order.save()

            if order.payment_method == "online":
                return redirect("payment_checkout", order_id=order.order_id)

            return redirect("order_success", order_id=order.order_id)

    else:
        initial_data = {}

        if request.user.is_authenticated and hasattr(request.user, "profile"):
            if request.user.profile.phone_number:
                initial_data["phone_number"] = request.user.profile.phone_number

            if request.user.first_name:
                initial_data["customer_name"] = request.user.get_full_name() or request.user.username

        form = OrderForm(initial=initial_data)

    return render(request, "orders/place_order.html", {"form": form})


def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, "orders/order_success.html", {"order": order})


def track_order(request):
    form = TrackOrderForm()
    error = None

    if request.method == "POST":
        form = TrackOrderForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data["order_id"]
            phone_number = form.cleaned_data["phone_number"]

            try:
                order = Order.objects.get(order_id=order_id, phone_number=phone_number)
                return redirect("order_detail", order_id=order.order_id)
            except Order.DoesNotExist:
                error = "No order found with this Order ID and phone number."

    return render(request, "orders/track_order.html", {"form": form, "error": error})


def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, "orders/order_detail.html", {"order": order})


def payment_checkout(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, "orders/payment_checkout.html", {"order": order})


def mark_payment_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order.payment_status = "paid"
    order.status = "confirmed"
    order.save()
    return redirect("order_success", order_id=order.order_id)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()

    return redirect("staff_dashboard")