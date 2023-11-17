from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DenoiseProcessViewSet,DenoiseResultViewSet

router = DefaultRouter()

router.register('denoise-process', DenoiseProcessViewSet)
router.register('denoise-result', DenoiseResultViewSet)

urlpatterns = [
    path('', include(router.urls))
]