from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from apps.ponno.models.brand import Brand
from apps.ponno.models.category import Category
from apps.ponno.models.product import Product
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView
from django.utils import timezone
import uuid

User = get_user_model()

def HomeView(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.all().select_related('category', 'brand')
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # Keyword search
    highlighted_products = []
    if query:
        keywords = query.split()
        q_object = Q()
        for word in keywords:
            q_object |= (
                Q(product_name__icontains=word) |
                Q(category__category_name__icontains=word) |
                Q(brand__brand_name__icontains=word) 
                
            )
        products = products.filter(q_object).distinct()

        # Prepare highlighted names
        for p in products:
            highlighted_name = p.product_name
            for word in keywords:
                if word.lower() in highlighted_name.lower():
                    highlighted_name = highlighted_name.replace(
                        word, f"<mark>{word}</mark>"
                    )
            p.highlighted_name = highlighted_name
            highlighted_products.append(p)
    else:
        highlighted_products = products

    # Pagination
    paginator = Paginator(highlighted_products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'query': query,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        
    }
    return render(request, "ponno/home.html", context)
