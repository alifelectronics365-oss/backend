
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from apps.customer.validators import email_or_phone_validator
from django.contrib.auth import get_user_model

User = get_user_model()
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.customer.models.profile_info import ProfileInfo
from apps.customer.models.account import User

from apps.ponno.models.brand import Brand
from apps.ponno.models.category import Category
from apps.ponno.models.product import Product

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.customer.models.profile_info import ProfileInfo
from apps.customer.models.account import User
from apps.ponno.models.brand import Brand
from apps.ponno.models.category import Category
from apps.ponno.models.product import Product


@login_required(login_url='/accounts/signin/')
def NotificationView(request):
    user = request.user
    
    # User profile
    profile_info = get_object_or_404(ProfileInfo, user=user)
    followings_count = profile_info.following.count()
    followers_count = profile_info.followers.count()

    # Product counts for dealer role users
    products_listed_count = Product.objects.filter(dealer=user).count()
    active_products_count = Product.objects.filter(dealer=user, is_active=True).count()

    # Global stats
    brands_count = Brand.objects.count()
    categories_count = Category.objects.count()
    brands = Brand.objects.all()
    categories = Category.objects.all()

    # ---------------------------------------------------
    #  🔔 WELCOME NOTIFICATION (Display only once)
    # ---------------------------------------------------
    notifications = []

    if hasattr(user, "welcome"):
        welcome = user.welcome

        if not welcome.is_shown:
            # Add welcome message to notification list
            notifications.append({
                "title": welcome.title,
                "message": welcome.message,
                "type": "success",   # used for CSS/Bootstrap classes
            })

            # Also add to Django messages framework (optional)
            messages.success(request, welcome.message)

            # Mark as shown
            welcome.is_shown = True
            welcome.save()

    # ---------------------------------------------------
    # In future: Add more notifications here
    # Example:
    # notifications.append({ "title": "New Order", "message": "You received an order.", "type": "info" })
    # ---------------------------------------------------

    context = {
        "user": user,
        "profile_info": profile_info,
        "followings_count": followings_count,
        "followers_count": followers_count,
        "products_listed_count": products_listed_count,
        "active_products_count": active_products_count,
        "brands_count": brands_count,
        "categories_count": categories_count,
        "brands": brands,
        "categories": categories,

        # NEW: Pass notifications to template
        "notifications": notifications,
    }

    return render(request, "notify/notification.html", context)
