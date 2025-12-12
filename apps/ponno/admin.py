from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from apps.customer.models.account import User
from apps.ponno.models.brand import Brand
from apps.ponno.models.category import Category
from apps.ponno.models.product import Product
# write your import here
from django.contrib import admin
 
from django.utils.html import format_html
from django.utils.text import slugify


# Register your models here.

# ------------------------------------------------------------
# BRAND ADMIN
# ------------------------------------------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'brand_name',
        'brand_slug',
        'brand_created_at',
        'brand_updated_at',
    )
    search_fields = ('brand_name',)
    prepopulated_fields = {'brand_slug': ('brand_name',)}
    ordering = ('brand_name',)
    readonly_fields = ('brand_created_at', 'brand_updated_at')


# ------------------------------------------------------------
# CATEGORY ADMIN
# ------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_name',
        'category_slug',
        'category_created_at',
        'category_updated_at',
    )
    search_fields = ('category_name',)
    prepopulated_fields = {'category_slug': ('category_name',)}
    ordering = ('category_name',)
    readonly_fields = ('category_created_at', 'category_updated_at')




# ------------------------------------------------------------
# PRODUCT ADMIN
# ------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="70" height="70" style="object-fit:cover;border-radius:5px;"/>',
                obj.image.url,
            )
        return "(No image)"

    image_preview.short_description = 'Preview'

    list_display = (
        'image_preview',
        'product_id',
        'product_name',
        'slug',
        'category',
        'brand',
  
        
        'buying_price',
        'brand_price',
        'selling_price',
        'stock',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_filter = ('brand', 'category', 'is_active')
    search_fields = ('product_id','product_name', 'brand__brand_name', 'category__category_name')
    list_editable = ('is_active', 'stock', 'buying_price', 'brand_price', 'selling_price')
    ordering = ('product_name',)
    readonly_fields = ('created_at', 'updated_at', 'product_id', 'slug')


