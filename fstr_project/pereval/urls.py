from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerevalCreateViewset

router = DefaultRouter()
router.register(r'create_pereval', PerevalCreateViewset, basename='create_pereval')

urlpatterns = [
    path('', include(router.urls)),
]
