import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings  # To refer to your AUTH_USER_MODEL
from apps.ponno.models.brand import Brand
from apps.ponno.models.category import Category

class Product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product_name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)

    brand = models.ForeignKey(
        Brand,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='products'
    )
    dealer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'dealer'},
        on_delete=models.CASCADE,
        related_name='products'
    )

    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    brand_price = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['product_name']

    def __str__(self):
        return f"{self.product_name} ({self.brand})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.product_name}-{self.brand}")
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)