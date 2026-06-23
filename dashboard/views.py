from django.shortcuts import render
from orders.models import Order


def dashboard_home(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()
    completed_orders = Order.objects.filter(status="completed").count()
    confirmed_orders = Order.objects.filter(status="confirmed").count()
    printing_orders = Order.objects.filter(status="printing").count()
    ready_orders = Order.objects.filter(status="ready").count()

    total_revenue = sum(order.total_price for order in Order.objects.filter(status="completed"))

    recent_orders = Order.objects.select_related("service").order_by("-created_at")[:8]

    context = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "confirmed_orders": confirmed_orders,
        "printing_orders": printing_orders,
        "ready_orders": ready_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
    }
    return render(request, "dashboard/home.html", context)