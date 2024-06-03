from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .resources import default_status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalUser
        fields = ['surname', 'name', 'otc', 'email', 'phone']


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalCoordinate
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalLevel
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImageSerializer(serializers.ModelSerializer):
    data = serializers.URLField()
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Image
        fields = ['title', 'data', 'add_time']


class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coord = CoordinateSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'beauty_title', 'title', 'other_title', 'connect', 'add_time', 'status',
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
        pereval = PerevalAdded.objects.create(user=user, coord=coord, level=level, **validated_data)

        for image_data in images_data:
            Image.objects.create(pereval=pereval, **image_data)

        return pereval

    def validate (self, data):
        if self.instance:
            if self.instance.status != default_status:
                raise serializers.ValidationError("Можно редактировать только записи со статусом 'new'")

            user_data = data.get('user', {})
            if user_data:
                user_fields = ['surname', 'name', 'otc', 'email', 'phone']
                for field in user_fields:
                    if field in user_data and getattr(self.instance.user, field) != user_data[field]:
                        raise serializers.ValidationError("Данные о пользователе невозможно изменить")

        return data
