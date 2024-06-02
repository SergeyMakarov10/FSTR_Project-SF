from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerevalCreateViewset, UserViewset, CoordinateViewset, \
    LevelViewset, ImageViewset

router = DefaultRouter()
router.register(r'create_pereval', PerevalCreateViewset, basename='create_pereval')
router.register(r'users', UserViewset)
router.register(r'coordinates', CoordinateViewset)
router.register(r'levels', LevelViewset)
router.register(r'images', ImageViewset)

urlpatterns = [
    path('', include(router.urls)),
]
