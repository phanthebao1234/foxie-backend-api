from django.contrib import admin
from .models import Category, Album, Image, User

admin.site.register(Category)
admin.site.register(Album)
admin.site.register(Image)
admin.site.register(User)
