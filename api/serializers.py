from rest_framework import serializers
from .models import User, Category, Album, Image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'thumbnail', 'caption']
        
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
            'images'
        ]

class CategorySerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'cover_image',
            'description',
            'albums'
        ]
        
class MultiImageUploadSerializer(serializers.Serializer):
    album = serializers.IntegerField()
    images = serializers.ListField(
        child=serializers.ImageField()
    )

    def create(self, validated_data):
        from .models import Album
        request = self.context.get('request')
        album = Album.objects.get(id=validated_data['album'])

        images = validated_data['images']
        objs = []

        for img in images:
            objs.append(Image.objects.create(
                album=album,
                image=img,
                uploaded_by=request.user
            ))

        return objs