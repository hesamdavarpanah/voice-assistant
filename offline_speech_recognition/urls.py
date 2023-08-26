from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CRUDVoiceViewSet, VoiceDetectionViewSet

router = DefaultRouter()

router.register('crud-voice', CRUDVoiceViewSet)
router.register('voice-detection', VoiceDetectionViewSet)

urlpatterns = [
    path('', include(router.urls))
]
