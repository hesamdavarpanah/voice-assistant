from django.db import models

from voice_manager.models import Voice


class HighDenoiseResult(models.Model):
    output_channels = models.IntegerField()
    output_sr = models.IntegerField()
    file_extension = models.CharField(max_length=10)
    publish_date = models.DateTimeField(auto_now_add=True)
    output_file = models.FilePathField(path='voice_split/output_files/')
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE, related_name='high_denoise_results')


class LowDenoiseResult(models.Model):
    output_channels = models.IntegerField()
    output_sr = models.IntegerField()
    file_extension = models.CharField(max_length=10)
    publish_date = models.DateTimeField(auto_now_add=True)
    vocal_file = models.FilePathField(path='voice_split/output_files/')
    instrument_file = models.FilePathField(path='voice_split/output_files/')
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE, related_name='low_denoise_results')
