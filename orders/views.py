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
            return redirect("order_success", order_id=order.order_id)
    else:
        form = OrderForm()

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