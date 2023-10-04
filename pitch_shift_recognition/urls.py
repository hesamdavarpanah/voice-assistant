from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PitchShiftViewSet

router = DefaultRouter()

router.register(r'result/(?P<voice_id>\d+)', PitchShiftViewSet)
# router.register(r'download-file/(?P<voice_id>\d+)', PitchShiftViewSet)

urlpatterns = [
    path('', include(router.urls))
]
