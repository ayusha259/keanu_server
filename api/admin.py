from django.contrib import admin
from .models import Product, ProductImage, Review, Order, OrderItem, ShippingAddress

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_filter = ("isOffer", "brand", "category", "user")
    list_display = ("title", "user")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline, ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)