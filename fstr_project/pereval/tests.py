from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import PerevalSerializer
from .models import *

class PerevalCreateTest(APITestCase):

    def setUp(self):
        self.valid_payload = {
            "beauty_title": "Перевал",
            "title": "Большой перевал",
            "other_title": "Малый перевал",
            "connect": "Соединяет долины",
            "user": {
                "email": "test@example.com",
                "surname": "Иванов",
                "name": "Иван",
                "otc": "Иванович",
                "phone": "1234567890"
            },
            "coord": {
                "latitude": 45.0,
                "longitude": 90.0,
                "height": 1200
            },
            "level": {
                "winter": "1a",
                "spring": "1b",
                "summer": "2a",
                "autumn": "2b"
            },
            "images": [
                {
                    "title": "Вид на перевал",
                    "data": "http://example.com/image.jpg"
                }
            ]
        }

    def test_create_pereval(self):
        url = reverse('create_pereval-list')
        response = self.client.post(url, self.valid_payload, format='json')
        print("Response data:", response.data)  # Добавляем вывод данных ответа для отладки

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 200)
        self.assertIsNotNone(response.data['id'])  # Проверяем, что id не None

        pereval = PerevalAdded.objects.get()
        self.assertEqual(pereval.title, 'Большой перевал')

        images = Image.objects.filter(pereval=pereval)
        self.assertEqual(images.count(), 1)
        self.assertEqual(images[0].title, 'Вид на перевал')
        self.assertEqual(images[0].data, 'http://example.com/image.jpg')
