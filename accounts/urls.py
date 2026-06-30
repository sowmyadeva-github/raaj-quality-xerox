from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    customer_dashboard,
    staff_dashboard,
    customer_profile,
    my_orders,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("customer/profile/", customer_profile, name="customer_profile"),

    path(
        "customer/dashboard/",
        customer_dashboard,
        name="customer_dashboard",
    ),

    path(
        "staff/dashboard/",
        staff_dashboard,
        name="staff_dashboard",
    ),
    path(
    "customer/orders/",
    my_orders,
    name="my_orders",
),
]