from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import ServicePackage, User, Category, Album, Image
from .serializers import MultiImageUploadSerializer, ServicePackageListSerializer, ServicePackageSerializer, UserSerializer, CategorySerializer, AlbumSerializer, ImageSerializer

class PublicReadAdminWriteViewSet(viewsets.ModelViewSet):
    """
    - GET: public
    - POST/PUT/PATCH/DELETE: cần login
    """

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
class AdminCategoryViewSet(PublicReadAdminWriteViewSet):
    queryset = Category.objects.prefetch_related('albums__images')
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Category.objects.filter(is_active=True)
        return Category.objects.all()

class AdminAlbumViewSet(PublicReadAdminWriteViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Album.objects.filter(is_public=True)
        return Album.objects.all()

class AdminImageViewSet(PublicReadAdminWriteViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Image.objects.filter(is_public=True)
        return Image.objects.all()
    
class MultiUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MultiImageUploadSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        images = serializer.save()
        return Response({
            "message": "Upload thành công", 
            "count": len(images)
        })
        
class ServicePackageViewSet(viewsets.ModelViewSet):
    queryset = ServicePackage.objects.all()
    lookup_field = 'slug'  # 🔥 dùng slug thay vì id

    # 🔎 filter theo category
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    # 📦 chọn serializer theo action
    def get_serializer_class(self):
        if self.action == 'list':
            return ServicePackageListSerializer
        return ServicePackageSerializer

    # 🔐 permission
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    # ⚡ tối ưu query
    def get_queryset(self):
        base_qs = ServicePackage.objects.select_related('category')\
            .prefetch_related('albums__images')

        if self.action in ['list', 'retrieve']:
            return base_qs.filter(is_active=True)

        return base_qs

    # 🧠 đảm bảo serializer có request (quan trọng cho image URL)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context