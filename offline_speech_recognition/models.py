from django.db import models
from django.contrib.auth.models import User
from voice_manager.models import Voice


class VoiceResult(models.Model):
    voice = models.ForeignKey(to=Voice, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)


class VoiceDetail(models.Model):
    publish_date = models.DateTimeField(auto_now_add=True)
    detect_time = models.FloatField()
    command_detected = models.CharField(max_length=150)
    voice_result = models.ForeignKey(to=VoiceResult, on_delete=models.CASCADE, related_name='voice_details')
