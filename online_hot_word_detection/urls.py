from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OnlineHotWordDetectionViewSet, SystemDeviceViewSet

router = DefaultRouter()

router.register('online-hot-word-detection', OnlineHotWordDetectionViewSet, basename="online-hot-word-detection")
router.register('device-list', SystemDeviceViewSet)

urlpatterns = [
    path('', include(router.urls))
]
