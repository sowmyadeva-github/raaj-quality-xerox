from django.urls import path
from .views import (
    create_order,
    order_success,
    track_order,
    order_detail,
    payment_checkout,
    mark_payment_success,
)

urlpatterns = [
    path("place/", create_order, name="place_order"),
    path("success/<str:order_id>/", order_success, name="order_success"),

    path("track/", track_order, name="track_order"),
    path("detail/<str:order_id>/", order_detail, name="order_detail"),

    path(
        "payment/<str:order_id>/",
        payment_checkout,
        name="payment_checkout",
    ),

    path(
        "payment-success/<str:order_id>/",
        mark_payment_success,
        name="payment_success",
    ),
]