from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import PerevalSerializer
from .models import *
import json
from django.test import TestCase


#Тесты для методов класса, отвечающие за работу с БД
class ModelTests(TestCase):

    def setUp(self):
        self.user = PerevalUser.objects.create(
            email="test@example.com", surname="Test", name="User", otc="Otch", phone="1234567890"
        )
        self.coord = PerevalCoordinate.objects.create(latitude=55.7558, longitude=37.6173, height=150)
        self.level = PerevalLevel.objects.create(winter="1a", spring="1b", summer="2a", autumn="2b")
        self.pereval = PerevalAdded.objects.create(
            beauty_title="Beautiful Pass", title="Test Pass", other_title="Other Test Pass",
            connect="Connect Info", user=self.user, coord=self.coord, level=self.level, status="new"
        )

    def test_create_pereval(self):
        self.assertEqual(PerevalAdded.objects.count(), 1)
        self.assertEqual(PerevalAdded.objects.first().title, "Test Pass")

    def test_update_pereval(self):
        self.pereval.title = "Updated Test Pass"
        self.pereval.save()
        self.pereval.refresh_from_db()
        self.assertEqual(self.pereval.title, "Updated Test Pass")

    def test_delete_pereval(self):
        self.pereval.delete()
        self.assertEqual(PerevalAdded.objects.count(), 0)

    def test_create_image(self):
        image = Image.objects.create(
            title="Test Image", data="http://example.com/image.jpg", pereval=self.pereval
        )
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(image.title, "Test Image")
        self.assertEqual(image.pereval, self.pereval)

    def test_update_image(self):
        image = Image.objects.create(
            title="Test Image", data="http://example.com/image.jpg", pereval=self.pereval
        )
        image.title = "Updated Test Image"
        image.save()
        image.refresh_from_db()
        self.assertEqual(image.title, "Updated Test Image")

    def test_delete_image(self):
        image = Image.objects.create(
            title="Test Image", data="http://example.com/image.jpg", pereval=self.pereval
        )
        image.delete()
        self.assertEqual(Image.objects.count(), 0)


#Тесты для REST API
class PerevalAPITests(APITestCase):
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
            "status": "new",
            "user": {
                "surname": "Test",
                "name": "User",
                "otc": "Otch",
                "email": "test@example.com",
                "phone": "1234567890"
            },
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

        self.invalid_payload_status = self.valid_payload.copy()
        self.invalid_payload_status['status'] = "accepted"

    def test_create_pereval(self):
        url = reverse('pereval-list')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])

    def test_update_pereval(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_new.id})
        response = self.client.patch(url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_pereval_invalid_user(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_new.id})
        response = self.client.patch(url, data=self.invalid_payload_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_error', response.data['errors'])
        self.assertEqual(response.data['message'], "Данные о пользователе невозможно изменить")

    def test_update_pereval_invalid_status(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_accepted.id})
        response = self.client.patch(url, data=self.invalid_payload_status, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status_error', response.data['errors'])
        self.assertEqual(response.data['message'], "Можно редактировать только записи со статусом 'new'")

    def test_get_pereval(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_new.id})
        response = self.client.get(url)
        print(f"Get By Id Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['beauty_title'], self.pereval_new.beauty_title)
        self.assertEqual(response.data['title'], self.pereval_new.title)
        self.assertEqual(response.data['status'], self.pereval_new.status)

    def test_get_perevals_by_user(self):
        url = reverse('pereval-list')
        response = self.client.get(url, {'user__email': 'test@example.com'})
        print(f"Get By User Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Убедитесь, что возвращены обе записи

        for pereval in response.data:
            self.assertEqual(pereval['user']['email'], 'test@example.com')
