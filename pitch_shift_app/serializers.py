from rest_framework.serializers import ModelSerializer
from .models import PitchShiftResult


class PitchShiftResultSerializers(ModelSerializer):
    class Meta:
        model = PitchShiftResult
        fields = '__all__'
