from os import path, makedirs

from celery import shared_task
from django.contrib.auth.models import User
from voice_split.voice_splitter.high_denoise import Denoiser

from voice_gallery.models import Voice
from .models import DenoiseResult


@shared_task()
def denoise_task(voice_id, file_extension):
    user = User.objects.get(username=request.user.username)
    voice = Voice.objects.get(id=voice_id, user=user)
    """
        put your denoise algorithm here
    """
    info = "load your denoise func here that could send json response"
    denoise = DenoiseResult.objects.create(output_file=info['output_file'],
                                                    output_sr=info['output_sr'],
                                                    output_channels=info['output_channels'],
                                                    file_extension=file_extension,
                                                    voice=voice)
    denoise.save()
