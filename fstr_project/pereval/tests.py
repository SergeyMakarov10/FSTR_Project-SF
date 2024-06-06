from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import PerevalSerializer
from .models import *
import json
from django.test import TestCase


#Тесты для методов класса, отвещающие за работу с БД
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

