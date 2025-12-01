from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        email_or_phone = request.POST.get("email_or_phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role", "customer")  # default role customer

        # Basic validation
        if not email_or_phone or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "customer/signup.html")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "customer/signup.html")

        # Check if user already exists
        if User.objects.filter(email_or_phone=email_or_phone).exists():
            messages.error(request, "User with this email or phone already exists.")
            return render(request, "customer/signup.html")

        # Create user
        user = User(
            email_or_phone=email_or_phone,
            role=role,
            is_active=True
        )
        user.set_password(password1)
        user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("customer:signin")  # adjust if you have signin url

    return render(request, "customer/signup.html")
