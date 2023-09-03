from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CRUDVoiceViewSet, OfflineVoiceDetectionViewSet

router = DefaultRouter()

router.register('crud-voice', CRUDVoiceViewSet)
router.register('voice-detection', OfflineVoiceDetectionViewSet)

urlpatterns = [
    path('', include(router.urls))
]
