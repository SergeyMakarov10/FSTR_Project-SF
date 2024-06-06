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
    # для метода patch не будет работать, нужно убрать read_only, но тогда PATCH не будет менять данные
    status = serializers.CharField()


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
                raise serializers.ValidationError({"status_error": "Можно редактировать только записи со статусом 'new'"})

            user_data = data.get('user', {})
            if user_data:
                user_fields = ['surname', 'name', 'otc', 'email', 'phone']
                for field in user_fields:
                    if field in user_data and getattr(self.instance.user, field) != user_data[field]:
                        raise serializers.ValidationError({"user_error":"Данные о пользователе невозможно изменить"})

        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        coord_data = validated_data.pop('coord', None)
        level_data = validated_data.pop('level', None)
        images_data = validated_data.pop('images', None)

        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_title = validated_data.get('other_title', instance.other_title)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.status = validated_data.get('status', instance.status)

        if user_data:
            UserSerializer().update(instance.user, user_data)
        if coord_data:
            CoordinateSerializer().update(instance.coord, coord_data)
        if level_data:
            LevelSerializer().update(instance.level, level_data)

        if images_data:
            # Удаляем старые изображения и добавляем новые
            instance.images.all().delete()
            for image_data in images_data:
                Image.objects.create(pereval=instance, **image_data)

        instance.save()
        return instance
