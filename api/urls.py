from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClothingCategoryViewSet, ClothingViewSet, MultiClothingUploadView, MultiUploadView, ServicePackageViewSet, UserViewSet, AdminCategoryViewSet, AdminAlbumViewSet, AdminImageViewSet

router = DefaultRouter()
# 👤 User
router.register('users', UserViewSet, basename='user')

# 📂 Categories
router.register('categories', AdminCategoryViewSet, basename='category')

# 📀 Albums
router.register('albums', AdminAlbumViewSet, basename='album')

# 🖼 Images
router.register('images', AdminImageViewSet, basename='image')

# 🎯 Packages (GÓI CHỤP)
router.register('packages', ServicePackageViewSet, basename='package')

router.register('clothing-categories', ClothingCategoryViewSet)
router.register('clothings', ClothingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # 📸 Upload nhiều ảnh
    path('upload-images/', MultiUploadView.as_view(), name='upload-images'),
    path('clothings/upload-images/', MultiClothingUploadView.as_view()),
]