from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalUser
        fields = ['surname', 'name', 'ots', 'email', 'phone']


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalCoordinate
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalLevel
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImageSerializer(serializers.ModelSerializer):
    data = serializers.ImageField()
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    class Meta:
        model = Image
        field = ['title', 'data', 'add_time']


class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coord = CoordinateSerializer()
    level = LevelSerializer
    images = ImageSerializer(many=True)
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = PerevalAdded
        fields = ['beauty_title', 'title', 'other_title', 'connect', 'add_time', 'status',
                  'user', 'coord', 'level', 'images',
                  ]

        def create(self, validated_data):
            user_data = validated_data.pop('user')
            coord_data = validated_data.pop('coord')
            level_data = validated_data.pop('level')
            images_data = validated_data.pop('images')

            user, created = PerevalUser.objects.get_or_create(**user_data)
            coord = PerevalCoordinate.objects.create(**coord_data)
            level = PerevalLevel.objects.create(**level_data)
            images_data = PerevalAdded.objects.create(user=user, coord=coord, level=level, **validated_data)

            for image_data in images_data:
                Image.objects.create(pereval=pereval, **image_data)

            return pereval