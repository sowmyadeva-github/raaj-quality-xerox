from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("customer_dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")

            if hasattr(user, "profile"):
                if user.profile.role == "owner":
                    return redirect("dashboard_home")
                elif user.profile.role == "staff":
                    return redirect("staff_dashboard")
                else:
                    return redirect("customer_dashboard")

            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")


def customer_dashboard(request):
    from orders.models import Order

    all_user_orders = Order.objects.filter(
        phone_number=request.user.profile.phone_number
    ).select_related("service")

    recent_orders = all_user_orders[:5]

    context = {
        "user_orders": recent_orders,
        "total_orders": all_user_orders.count(),
        "active_orders": all_user_orders.exclude(status__in=["completed", "cancelled"]).count(),
        "completed_orders": all_user_orders.filter(status="completed").count(),
        "pending_payments": all_user_orders.filter(payment_status="pending").count(),
    }

    return render(request, "accounts/customer_dashboard.html", context)


@login_required

def staff_dashboard(request):
    from orders.models import Order

    active_orders = Order.objects.exclude(
        status__in=["completed", "cancelled"]
    ).select_related("service")

    context = {
        "active_orders": active_orders,
        "active_count": active_orders.count(),
        "pending_count": Order.objects.filter(status="pending").count(),
        "printing_count": Order.objects.filter(status="printing").count(),
        "ready_count": Order.objects.filter(status="ready").count(),
    }

    return render(request, "accounts/staff_dashboard.html", context)
@login_required
def customer_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("customer_profile")

    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/customer_profile.html",
        {
            "form": form,
        },
    )
@login_required
def my_orders(request):
    from orders.models import Order

    orders = Order.objects.filter(
        phone_number=request.user.profile.phone_number
    ).select_related("service")

    return render(
        request,
        "accounts/my_orders.html",
        {
            "orders": orders,
        },
    )