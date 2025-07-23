from django.db import models
from django.utils.text import slugify
from uuid import uuid4
from cloudinary.models import CloudinaryField
from django.conf import settings


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    product_image = CloudinaryField(folder='Dashboard/products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        base_slug = slugify(self.name)
        slug = base_slug
        num = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{num}'
            num += 1
        self.slug = slug

        if self.stock_quantity == 0:
            self.is_available = False

        super().save(*args, **kwargs)