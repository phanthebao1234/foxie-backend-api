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