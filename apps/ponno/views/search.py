from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from apps.ponno.models.product import Product

@require_GET
def AjaxSearchView(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)

    keywords = query.split()
    q_object = Q()
    for word in keywords:
        q_object |= (
            Q(product_name__icontains=word) |
            Q(category__category_name__icontains=word) |
            Q(brand__brand_name__icontains=word)
        )
    products = Product.objects.filter(q_object).select_related('category', 'brand').distinct()

    results = []
    for p in products[:10]:
        results.append({
            "name": p.product_name,
            "slug": p.slug,
            "category": p.category.category_name,
            "brand": p.brand.brand_name,
            "brand_price": str(p.brand_price) if p.brand_price else None,
            "selling_price": str(p.selling_price) if p.selling_price else None,
            "image": p.image.url if p.image else "/static/ponno/img/no-image.png"
        })

    return JsonResponse(results, safe=False)
