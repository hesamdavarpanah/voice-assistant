from rest_framework.serializers import ModelSerializer
from .models import Voice


class VoiceSerializer(ModelSerializer):
    class Meta:
        model = Voice
        fields = "__all__"
