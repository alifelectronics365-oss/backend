
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView
from django.utils import timezone
import uuid
from apps.ponno.models.product import Product
from apps.ponno.models.category import Category
from apps.ponno.models.brand import Brand

def BrandProducts(request, brand_slug):
    
    """Show all products of a specific brand."""
    brand = get_object_or_404(Brand, brand_slug=brand_slug)
    products = Product.objects.filter(brand=brand, is_active=True).select_related('category', 'brand')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'query': '',
        'selected_brand': brand,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        
        
        
    }
    return render(request, 'ponno/home.html', context)
