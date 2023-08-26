from django.db import models
from django.contrib.auth.models import User


class Voice(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    voice_file = models.FileField(upload_to="user_voices/")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class VoiceResult(models.Model):
    voice = models.ForeignKey(to=Voice, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    result_voice_file = models.FilePathField()


class VoiceDetail(models.Model):
    publish_date = models.DateTimeField(auto_now_add=True)
    detect_time = models.FloatField()
    command_detected = models.CharField(max_length=150)
    voice_result = models.ForeignKey(to=VoiceResult, on_delete=models.CASCADE, related_name='voice_details')
