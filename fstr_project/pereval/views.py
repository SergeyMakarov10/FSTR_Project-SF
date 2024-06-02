from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import UserSerializer, CoordinateSerializer, LevelSerializer, \
    PerevalSerializer, ImageSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = PerevalUser.objects.all()
    serializer_class = UserSerializer


class CoordinateViewset(viewsets.ModelViewSet):
    queryset = PerevalCoordinate.objects.all()
    serializer_class = CoordinateSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = PerevalLevel.objects.all()
    serializer_class = LevelSerializer


class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class PerevalCreateViewset(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer

    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 200,
                'message': '',
                'id': serializer.data.get('id')
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            response_data = {
                'status': 400,
                'message': 'Неверный запрос',
                'errors': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
