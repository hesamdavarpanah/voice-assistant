from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HighDenoiseProcessViewSet, HighDenoiseResultViewSet, LowDenoiseProcessViewSet, \
    LowDenoiseResultViewSet

router = DefaultRouter()

router.register('high-denoise-process', HighDenoiseProcessViewSet)
router.register('high-denoise-result', HighDenoiseResultViewSet)
router.register('low-denoise-result', LowDenoiseResultViewSet)
router.register('low-denoise-process', LowDenoiseProcessViewSet)

urlpatterns = [
    path('', include(router.urls))
]
