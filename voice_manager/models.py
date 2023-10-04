from django.db import models
from django.contrib.auth.models import User


class Voice(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    voice_file = models.FileField(upload_to="user_voices/")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
