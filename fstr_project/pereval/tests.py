from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import PerevalSerializer
from .models import *
import json

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


class PerevalUpdateTest(APITestCase):
    def setUp(self):
        self.user = PerevalUser.objects.create(
            email="test@example.com", surname="Test", name="User", otc="Otch", phone="1234567890"
        )
        self.coord_new = PerevalCoordinate.objects.create(latitude=55.7558, longitude=37.6173, height=150)
        self.coord_accepted = PerevalCoordinate.objects.create(latitude=56.7558, longitude=38.6173, height=160)
        self.level = PerevalLevel.objects.create(winter="1a", spring="1b", summer="2a", autumn="2b")
        self.pereval_new = PerevalAdded.objects.create(
            beauty_title="Beautiful Pass", title="Test Pass", other_title="Other Test Pass",
            connect="Connect Info", user=self.user, coord=self.coord_new, level=self.level, status="new"
        )
        self.pereval_accepted = PerevalAdded.objects.create(
            beauty_title="Accepted Pass", title="Accepted Pass", other_title="Other Accepted Pass",
            connect="Accepted Connect Info", user=self.user, coord=self.coord_accepted, level=self.level, status="accepted"
        )

        self.valid_payload = {
            "beauty_title": "Updated Beautiful Pass",
            "title": "Updated Test Pass",
            "other_title": "Updated Other Test Pass",
            "connect": "Updated Connect Info",
            "coord": {
                "latitude": 57.7558,
                "longitude": 39.6173,
                "height": 200
            },
            "level": {
                "winter": "2a",
                "spring": "2b",
                "summer": "3a",
                "autumn": "3b"
            },
            "images": [
                {
                    "title": "Image 1",
                    "data": "https://example.com/image1.jpg"
                },
                {
                    "title": "Image 2",
                    "data": "https://example.com/image2.jpg"
                }
            ]
        }

        self.invalid_payload_user = self.valid_payload.copy()
        self.invalid_payload_user['user'] = {
            "email": "newemail@example.com",
            "surname": "NewSurname",
            "name": "NewName",
            "otc": "NewOtch",
            "phone": "0987654321"
        }

    def test_partial_update_pereval(self):
        url = reverse('update_pereval-detail', kwargs={'pk': self.pereval_new.id})
        response = self.client.patch(url, data=json.dumps(self.valid_payload), content_type='application/json')
        print(f"Response data: {response.data}")  # Отладочное сообщение
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 1)

        # Убедитесь, что запись была обновлена
        self.pereval_new.refresh_from_db()
        self.assertEqual(self.pereval_new.beauty_title, self.valid_payload['beauty_title'])
        self.assertEqual(self.pereval_new.title, self.valid_payload['title'])
        self.assertEqual(self.pereval_new.other_title, self.valid_payload['other_title'])
        self.assertEqual(self.pereval_new.connect, self.valid_payload['connect'])

        # Убедитесь, что координаты были обновлены
        self.assertEqual(self.pereval_new.coord.latitude, self.valid_payload['coord']['latitude'])
        self.assertEqual(self.pereval_new.coord.longitude, self.valid_payload['coord']['longitude'])
        self.assertEqual(self.pereval_new.coord.height, self.valid_payload['coord']['height'])

        # Убедитесь, что уровни сложности были обновлены
        self.assertEqual(self.pereval_new.level.winter, self.valid_payload['level']['winter'])
        self.assertEqual(self.pereval_new.level.spring, self.valid_payload['level']['spring'])
        self.assertEqual(self.pereval_new.level.summer, self.valid_payload['level']['summer'])
        self.assertEqual(self.pereval_new.level.autumn, self.valid_payload['level']['autumn'])

        # Убедитесь, что изображения были обновлены
        self.assertEqual(self.pereval_new.images.count(), len(self.valid_payload['images']))
        for image, image_data in zip(self.pereval_new.images.all(), self.valid_payload['images']):
            self.assertEqual(image.title, image_data['title'])
            self.assertEqual(image.data, image_data['data'])

    def test_partial_update_pereval_user_data_error(self):
        url = reverse('update_pereval-detail', kwargs={'pk': self.pereval_new.id})
        response = self.client.patch(url, data=json.dumps(self.invalid_payload_user), content_type='application/json')
        print(f"Response data: {response.data}")  # Отладочное сообщение
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_error', response.data['errors'])
        self.assertEqual(response.data['message'], "Данные о пользователе невозможно изменить")

    def test_partial_update_pereval_status_error(self):
        url = reverse('update_pereval-detail', kwargs={'pk': self.pereval_accepted.id})
        response = self.client.patch(url, data=json.dumps(self.valid_payload), content_type='application/json')
        print(f"Response data: {response.data}")  # Отладочное сообщение
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status_error', response.data['errors'])
        self.assertEqual(response.data['message'], "Можно редактировать только записи со статусом 'new'")