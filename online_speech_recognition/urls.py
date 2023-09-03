from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OnlineVoiceDetectionViewSet, SystemDeviceViewSet

router = DefaultRouter()

router.register('voice-detection', OnlineVoiceDetectionViewSet, basename="voice-detection")
router.register('device-list', SystemDeviceViewSet)

urlpatterns = [
    path('', include(router.urls))
]
