from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PitchShiftProcessViewSet, GetPitchShiftResultViewSet

router = DefaultRouter()

router.register('pitch-shift-process', PitchShiftProcessViewSet)
router.register('get-result', GetPitchShiftResultViewSet)

urlpatterns = [
    path('', include(router.urls))
]
