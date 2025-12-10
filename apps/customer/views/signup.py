from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.customer.validators import email_or_phone_validator, strong_password_validator
from apps.kobutor.email import send_welcome_email
from apps.kobutor.sms import send_welcome_sms 

User = get_user_model()


def SignUpView(request):
    if request.method == "POST":
        email_or_phone = request.POST.get("email_or_phone", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        role = request.POST.get("role", "customer")

        context = {
            'email_or_phone': email_or_phone,
            'role': role
        }

        # -------------------------
        # Validations
        # -------------------------
        if not email_or_phone or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "customer/signup.html", context)

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "customer/signup.html", context)

        try:
            email_or_phone_validator(email_or_phone)
        except ValidationError as e:
            messages.error(request, e.message)
            return render(request, "customer/signup.html", context)

        try:
            strong_password_validator(password1)
        except ValidationError as e:
            messages.error(request, e.message)
            return render(request, "customer/signup.html", context)

        # Check if exists
        if User.objects.filter(email_or_phone=email_or_phone).exists():
            messages.error(request, "User with this email or phone already exists.")
            return render(request, "customer/signup.html", context)

        # -------------------------
        # Create User
        # -------------------------
        try:
            user = User.objects.create_user(
                email_or_phone=email_or_phone,
                password=password1,
                role=role,
            )
        except Exception:
            messages.error(request, "Something went wrong while creating your account.")
            return render(request, "customer/signup.html", context)

        # -------------------------
        # Send welcome email if it's an email
        # -------------------------
        if user.role == "customer":
            if user.is_email:
                try:
                    send_welcome_email(user)
                    
                except Exception:
                    messages.warning(request, "Account created, but we couldn't send the welcome email.")
            elif user.is_phone():
                try: 
                   send_welcome_sms(user.email_or_phone)
                    
                except Exception:
                    messages.warning(request, "Account created, but we couldn't send the welcome SMS.")

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("customer:signin")

    return render(request, "customer/signup.html")
