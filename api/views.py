from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Clothing, ClothingCategory, ServicePackage, User, Category, Album, Image
from .serializers import ClothingCategorySerializer, ClothingSerializer, MultiClothingImageUploadSerializer, MultiImageUploadSerializer, ServicePackageListSerializer, ServicePackageSerializer, UserSerializer, CategorySerializer, AlbumSerializer, ImageSerializer

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
        base_qs = Album.objects.prefetch_related('images')

        if self.action in ['list', 'retrieve']:
            return base_qs.filter(is_public=True)

        return base_qs

class AdminImageViewSet(PublicReadAdminWriteViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        base_qs = Image.objects.select_related('album')

        if self.action in ['list', 'retrieve']:
            return base_qs.filter(is_public=True)

        return base_qs
    
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
    
class ClothingCategoryViewSet(PublicReadAdminWriteViewSet):
    queryset = ClothingCategory.objects.all()
    serializer_class = ClothingCategorySerializer
    
class ClothingViewSet(PublicReadAdminWriteViewSet):
    queryset = Clothing.objects.all()
    serializer_class = ClothingSerializer

    parser_classes = [MultiPartParser, FormParser]

    # 🔎 filter + search + sort (optional)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'size', 'color']
    search_fields = ['code', 'material']
    ordering_fields = ['rental_price', 'created_at']

    def get_queryset(self):
        return Clothing.objects.select_related('category')\
            .prefetch_related('images')
            
class MultiClothingUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MultiClothingImageUploadSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        images = serializer.save()

        return Response({
            "message": "Upload thành công",
            "count": len(images)
        })