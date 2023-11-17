from rest_framework.serializers import ModelSerializer
from .models import DenoiseResult


class DenoiseResultSerializers(ModelSerializer):
    class Meta:
        model = DenoiseResult
        fields = "__all__"
