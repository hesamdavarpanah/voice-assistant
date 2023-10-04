from rest_framework.serializers import ModelSerializer
from .models import PitchShiftResult


class PitchShiftResultSerializers(ModelSerializer):
    class Meta:
        model = PitchShiftResult
        fields = ['id', 'sample_rate', 'channel', 'file_format']


class PitchShiftResultFileSerializers(ModelSerializer):
    class Meta:
        model = PitchShiftResult
        fields = ['id', 'filename']