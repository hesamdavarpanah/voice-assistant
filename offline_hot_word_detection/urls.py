from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OfflineHotWordDetectionViewSet

router = DefaultRouter()

router.register(r'hot-word-detection/(?P<voice_id>\d+)', OfflineHotWordDetectionViewSet)

urlpatterns = [
    path('', include(router.urls))
]
