from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.customer.models.profile_info import ProfileInfo
from apps.ponno.models.brand import Brand
from apps.ponno.models.category import Category
from apps.ponno.models.product import Product


@login_required(login_url='/accounts/signin/')
def EditProfileView(request):
    user = request.user
    profile_info = get_object_or_404(ProfileInfo, user=user)

    followings_count = profile_info.following.count()
    followers_count = profile_info.followers.count()

    products_listed_count = Product.objects.filter(dealer=user).count()
    active_products_count = Product.objects.filter(dealer=user, is_active=True).count()

    brands_count = Brand.objects.count()
    categories_count = Category.objects.count()

    # ---------- HANDLE FORM SUBMISSION ----------
    if request.method == "POST":
        profile_name = request.POST.get("profile_name")
        profile_address = request.POST.get("profile_address")
        profile_gender = request.POST.get("profile_gender")
        profile_dob = request.POST.get("profile_dob")
        profile_language = request.POST.get("profile_language")

        profile_photo = request.FILES.get("profile_photo")
        profile_cover_photo = request.FILES.get("profile_cover_photo")

        # Save text fields
        profile_info.profile_name = profile_name
        profile_info.profile_address = profile_address
        profile_info.profile_gender = profile_gender
        profile_info.profile_language = profile_language

        # Save dob only if provided
        if profile_dob:
            profile_info.profile_dob = profile_dob

        # Save images only if uploaded
        if profile_photo:
            profile_info.profile_photo = profile_photo
        
        if profile_cover_photo:
            profile_info.profile_cover_photo = profile_cover_photo

        profile_info.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("customer:profile")

    # ---------- RENDER PAGE ----------
    context = {
        "user": user,
        "profile_info": profile_info,
        "followings_count": followings_count,
        "followers_count": followers_count,
        "products_listed_count": products_listed_count,
        "active_products_count": active_products_count,
        "brands_count": brands_count,
        "categories_count": categories_count,
        "brands": Brand.objects.all(),
        "categories": Category.objects.all(),
    }

    return render(request, "customer/profile_edit.html", context)
