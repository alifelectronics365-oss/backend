import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings  # To refer to your AUTH_USER_MODEL

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_slug = models.SlugField(unique=True, blank=True, null=True)
    category_created_at = models.DateTimeField(auto_now_add=True)
    category_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category_name']

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.category_slug:
            self.category_slug = slugify(self.category_name)
        super().save(*args, **kwargs)