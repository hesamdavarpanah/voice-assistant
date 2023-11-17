from rest_framework.serializers import ModelSerializer
from .models import VoiceResult, VoiceDetail


class VoiceDetailSerializer(ModelSerializer):
    class Meta:
        model = VoiceDetail
        fields = "__all__"


class VoiceResultSerializer(ModelSerializer):
    voice_details = VoiceDetailSerializer(many=True, read_only=False)

    class Meta:
        model = VoiceResult
        fields = ['id', 'publish_date', 'voice_details']
