from rest_framework.serializers import ModelSerializer
from .models import HighDenoiseResult, LowDenoiseResult


class HighDenoiseResultSerializers(ModelSerializer):
    class Meta:
        model = HighDenoiseResult
        fields = "__all__"


class LowDenoiseResultSerializers(ModelSerializer):
    class Meta:
        model = LowDenoiseResult
        fields = "__all__"
