from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('electrician', 'Electrician'),
        ('plumbing', 'Plumbing'),
        ('cleaning', 'Cleaning'),
        ('repair', 'Repair'),
        ('painting', 'Painting'),
        ('carpenter', 'Carpenter'),
        ('appliance', 'Appliance Repair'),
        ('pest_control', 'Pest Control'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    rating = models.FloatField(default=4.0)
    image = models.URLField(blank=True, null=True)


from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('plumber', 'Plumber'),
    ('electrician', 'Electrician'),
    ('cleaning', 'Cleaning'),
    ('beauty', 'Beauty Service'),
]

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    phone = models.CharField(max_length=15)
    experience_years = models.IntegerField(default=0)
    rating = models.FloatField(default=4.0)
    is_available = models.BooleanField(default=True)

    address = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='providers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    user_name = models.CharField(max_length=100)

    date = models.DateField(default=timezone.now)

    quantity = models.PositiveIntegerField(default=1)

    status = models.CharField(max_length=20, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.service.base_price + (
            self.quantity * self.service.price_per_unit
        )


class Payment(models.Model):
    PAYMENT_TYPE = (
        ("booking", "Booking"),
        ("product", "Product"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(max_length=20, default="created")

    # ⭐ THIS FIXES YOUR CONFUSION
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE,
        default="booking"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
from django.db import models

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('electrician', 'Electrician'),
        ('plumbing', 'Plumbing'),
        ('cleaning', 'Cleaning'),
    ]

    TAG_CHOICES = [
        ('bestseller', 'Bestseller'),
        ('premium', 'Premium'),
        ('new', 'New'),
        ('popular', 'Popular'),
        ('budget', 'Budget'),
        ('hot', 'Hot'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, blank=True)

    image = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name