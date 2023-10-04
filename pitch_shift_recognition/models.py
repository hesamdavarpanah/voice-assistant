from django.db import models
from voice_manager.models import Voice


class PitchShiftResult(models.Model):
    sample_rate = models.IntegerField()
    channel = models.IntegerField()
    file_extension = models.CharField(max_length=10, null=True)
    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    filename = models.FileField(upload_to="pitch_shift_voices/", null=True)
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE, related_name='pitch_shift_results')
