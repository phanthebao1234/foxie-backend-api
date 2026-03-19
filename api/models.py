from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    cover_image = models.ImageField(upload_to='category_covers/')
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='albums'
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    cover_image = models.ImageField(upload_to='album_covers/')
    description = models.TextField(blank=True)

    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
class Image(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='images/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)

    caption = models.CharField(max_length=255, blank=True)
    
    is_featured = models.BooleanField(default=False)  # ảnh nổi bật
    created_at = models.DateTimeField(auto_now_add=True)
    
class ServicePackage(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='packages'
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    price = models.DecimalField(max_digits=10, decimal_places=0)

    description = models.TextField()
    cover_image = models.ImageField(upload_to='packages/')
    
    background_image = models.ImageField(
        upload_to='packages/backgrounds/',
        blank=True,
        null=True
    )

    # liên kết album mẫu
    albums = models.ManyToManyField(
        'Album',
        related_name='packages',
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ClothingCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return self.name
    
class Clothing(models.Model):
    category = models.ForeignKey(
        ClothingCategory,
        on_delete=models.CASCADE,
        related_name='clothings'
    )

    code = models.CharField(max_length=50, unique=True)  # mã sản phẩm
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    material = models.CharField(max_length=100)

    rental_price = models.DecimalField(max_digits=10, decimal_places=0)

    status = models.CharField(
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('rented', 'Rented'),
            ('maintenance', 'Maintenance')
        ],
        default='available'
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    
class Clothing(models.Model):
    category = models.ForeignKey(
        ClothingCategory,
        on_delete=models.CASCADE,
        related_name='clothings'
    )

    code = models.CharField(max_length=50, unique=True)  # mã sản phẩm
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    material = models.CharField(max_length=100)

    rental_price = models.DecimalField(max_digits=10, decimal_places=0)

    status = models.CharField(
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('rented', 'Rented'),
            ('maintenance', 'Maintenance')
        ],
        default='available'
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    
class ClothingImage(models.Model):
    clothing = models.ForeignKey(
        Clothing,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='clothings/')
    created_at = models.DateTimeField(auto_now_add=True)