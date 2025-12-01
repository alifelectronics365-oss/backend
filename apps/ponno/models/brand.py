import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings  # To refer to your AUTH_USER_MODEL


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    brand_slug = models.SlugField(unique=True, blank=True)
    brand_created_at = models.DateTimeField(auto_now_add=True)
    brand_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['brand_name']

    def __str__(self):
        return self.brand_name

    def save(self, *args, **kwargs):
        if not self.brand_slug:
            self.brand_slug = slugify(self.brand_name)
        super().save(*args, **kwargs)