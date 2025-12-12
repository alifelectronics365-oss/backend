
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

def SignInView(request):
    if request.method == "POST":
        email_or_phone = request.POST.get("email_or_phone", "").strip()
        password = request.POST.get("password", "")

        if not email_or_phone or not password:
            messages.error(request, "Please enter both email/phone and password.")
            return render(request, "customer/signin.html", {"email_or_phone": email_or_phone})

        user = authenticate(request, username=email_or_phone, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {email_or_phone}!")
                # Redirect to some dashboard or home page after login
                return redirect("customer:profile")  # Replace 'home' with your desired URL name
            else:
                messages.error(request, "Your account is inactive. Please contact support.")
        else:
            messages.error(request, "Invalid email/phone or password.")

        return render(request, "customer/signin.html", {"email_or_phone": email_or_phone})

    return render(request, "customer/signin.html")
