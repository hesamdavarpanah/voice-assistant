from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CRUDVoiceViewSet

router = DefaultRouter()

router.register('crud-voice', CRUDVoiceViewSet)

urlpatterns = [
    path('', include(router.urls))
]
