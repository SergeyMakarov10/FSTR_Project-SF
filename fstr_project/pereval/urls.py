from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerevalViewset, UserViewset, CoordinateViewset, \
    LevelViewset, ImageViewset, PerevalDetailView
#PerevalUpdateViewset

router = DefaultRouter()
router.register(r'pereval', PerevalViewset, basename='pereval')
router.register(r'users', UserViewset)
router.register(r'coordinates', CoordinateViewset)
router.register(r'levels', LevelViewset)
router.register(r'images', ImageViewset)
# router.register(r'update_pereval', PerevalUpdateViewset, basename='update_pereval')

urlpatterns = [
    path('', include(router.urls)),
    path('perevals/<int:id>/', PerevalDetailView.as_view(), name='pereval-detail'),
]
