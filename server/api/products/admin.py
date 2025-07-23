from django.contrib import admin
from django.utils.html import format_html

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'stock_quantity', 'product_image_preview', 'owner', 'created_at')

    def product_image_preview(self, obj):
        if obj.product_image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:contain;" />',
                obj.product_image.url
            )
        return "No Image"

    product_image_preview.short_description = 'Product Image Preview'

admin.site.register(Product, ProductAdmin)