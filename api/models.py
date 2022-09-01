from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
class Product(models.Model):
    _id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    isOffer = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    countInStock = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default="", db_index=True, max_length=200)

    def __str__(self):
        return self.title

def product_image_path(instance, filename):
        return f"product_{instance.product._id}/{filename}"

class ProductImage(models.Model):
    image = CloudinaryField('images')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)

class Review(models.Model):
    _id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    _id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentMethod = models.CharField(max_length=50)
    taxPrice = models.DecimalField(max_digits=9, decimal_places=2)
    shippingPrice = models.DecimalField(max_digits=6, decimal_places=2, default=299)
    totalPrice = models.DecimalField(max_digits=12, decimal_places=2)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        date = self.created_at.strftime("%m/%d/%Y-%H:%M")
        return f"Order: {self.user}-{str(self._id)}-{date}"

class OrderItem(models.Model):
    _id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)

class ShippingAddress(models.Model):
    _id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    apt_no = models.CharField(max_length=10)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postalcode = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
