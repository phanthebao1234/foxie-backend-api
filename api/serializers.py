from rest_framework import serializers
from .models import ServicePackage, User, Category, Album, Image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        # POST: gửi password được
        # GET: không trả password (bảo mật)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'thumbnail', 'caption']
        
    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
        
class AlbumSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            'id',
            'name',
            'slug',
            'cover_image',
            'description',
            'images',
            'is_active',
            'created_at'
        ]

class CategorySerializer(serializers.ModelSerializer):
    albums = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'cover_image',
            'description',
            'albums',
            'is_active',
            'created_at'
        ]
        
class MultiImageUploadSerializer(serializers.Serializer):
    album = serializers.IntegerField()
    images = serializers.ListField(
        child=serializers.ImageField()
    )

    def validate_album(self, value):
        from .models import Album
        if not Album.objects.filter(id=value).exists():
            raise serializers.ValidationError("Album không tồn tại")
        return value

    def create(self, validated_data):
        from .models import Album, Image

        request = self.context.get('request')
        album = Album.objects.get(id=validated_data['album'])

        images = validated_data['images']

        objs = [
            Image(
                album=album,
                image=img,
                uploaded_by=request.user
            )
            for img in images
        ]

        return Image.objects.bulk_create(objs)
    
class ServicePackageSerializer(serializers.ModelSerializer):
    background_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ServicePackage
        fields = [
            'id',
            'name',
            'slug',
            'price',
            'description',
            'cover_image',
            'background_image',
            'background_image_url',
            'albums',
            'category',
            'is_active',
            'created_at'
        ]

    def get_background_image_url(self, obj):
        request = self.context.get('request')
        if obj.background_image:
            if request:
                return request.build_absolute_uri(obj.background_image.url)
            return obj.background_image.url
        return None
    
class ServicePackageListSerializer(serializers.ModelSerializer):
    background_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ServicePackage
        fields = [
            'id',
            'name',
            'slug',
            'price',
            'cover_image',
            'background_image_url'
        ]

    def get_background_image_url(self, obj):
        request = self.context.get('request')
        if obj.background_image:
            return request.build_absolute_uri(obj.background_image.url)
        return None
    
from rest_framework import serializers
from .models import Clothing, ClothingCategory, ClothingImage


class ClothingImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ClothingImage
        fields = ['id', 'image', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
    
class ClothingSerializer(serializers.ModelSerializer):
    images = ClothingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Clothing
        fields = [
            'id',
            'code',
            'category',
            'color',
            'size',
            'material',
            'rental_price',
            'status',
            'description',
            'images',
            'created_at',
            'updated_at'
        ]
        
class ClothingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothingCategory
        fields = ['id', 'name', 'slug']

class MultiClothingImageUploadSerializer(serializers.Serializer):
    clothing = serializers.IntegerField()
    images = serializers.ListField(
        child=serializers.ImageField()
    )
    def validate_clothing(self, value):
        if not Clothing.objects.filter(id=value).exists():
            raise serializers.ValidationError("Trang phục không tồn tại")
        return value
    
    def create(self, validated_data):
        from .models import Clothing, ClothingImage

        clothing = Clothing.objects.get(id=validated_data['clothing'])
        images = validated_data['images']

        objs = [
            ClothingImage(
                clothing=clothing,
                image=img
            )
            for img in images
        ]

        return ClothingImage.objects.bulk_create(objs)
    
class RecursiveCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = ClothingCategory
        fields = ['id', 'name', 'slug', 'children']

    def get_children(self, obj):
        return RecursiveCategorySerializer(
            obj.children.all(), many=True
        ).data