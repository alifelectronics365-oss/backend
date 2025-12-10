
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

def ProductDetail(request, slug):
    

    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
       
    }
    return render(request, 'ponno/product_detail.html', context)

