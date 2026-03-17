from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MultiUploadView, UserViewSet, CategoryViewSet, AlbumViewSet, ImageViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('albums', AlbumViewSet)
router.register('images', ImageViewSet)
path('admin/upload-images/', MultiUploadView.as_view()),

urlpatterns = router.urls