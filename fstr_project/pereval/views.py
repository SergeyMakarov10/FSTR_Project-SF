from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import UserSerializer, CoordinateSerializer, LevelSerializer, \
    PerevalSerializer, ImageSerializer
from .resources import default_status
from django.shortcuts import get_object_or_404


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


# Создание перевала
class PerevalViewset(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer

    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        try:
            if serializer.is_valid():
                pereval = serializer.save()
                response_data = {
                    'status': 200,
                    'message': '',
                    'id': pereval.id
                }
                print(f"Response data: {response_data}")  # Отладочное сообщение
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    'status': 400,
                    'message': 'Неверный запрос',
                    'errors': serializer.errors
                }
                print(f"Response data: {response_data}")  # Отладочное сообщение
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'status': 500,
                'message': 'Ошибка при выполнении операции',
                'errors': str(e)
            }
            print(f"Response data: {response_data}")  # Отладочное сообщение
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        serializer = PerevalSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 1,
                'message': 'Данные успешно изменены',
            }
            print(f"Response data: {response_data}")  # Отладочное сообщение
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Проверяем ошибки и формируем корректное сообщение
            if 'status_error' in serializer.errors:
                response_data = {
                    'status': 0,
                    'message': serializer.errors['status_error'][0],  # Извлекаем сообщение об ошибке статуса
                    'errors': serializer.errors
                }
            elif 'user_error' in serializer.errors:
                response_data = {
                    'status': 0,
                    'message': serializer.errors['user_error'][0],  # Извлекаем сообщение об ошибке пользователя
                    'errors': serializer.errors
                }
            else:
                response_data = {
                    'status': 0,
                    'message': 'Неверный запрос',
                    'errors': serializer.errors
                }

            print(f"Response data: {response_data}")  # Отладочное сообщение
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        user_email = self.request.query_params.get('user__email', None)
        if user_email is not None:
            queryset = queryset.filter(user__email=user_email)
        return queryset


# Получение одной записи (перевала) по её id
class PerevalDetailView(APIView):
    def get(self, request, id):
        pereval = get_object_or_404(PerevalAdded, id=id)
        serializer = PerevalSerializer(pereval)
        return Response(serializer.data, status=status.HTTP_200_OK)
