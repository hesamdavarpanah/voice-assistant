import numpy as np
import os
import wave
from celery import shared_task
from pydub import AudioSegment

from voice_gallery.models import Voice
from .models import VoiceResult, VoiceDetail


@shared_task()
def offline_inference(wave_file, voice_id, step=0.25, window_size=2.0):
    try:
        """
            put your hot word detection algorithm here
        """
        split_text = wave_file.split('convert_')[-1]
        name = split_text.split('.')[0]
        voice = Voice.objects.get(id=voice_id)
        voice_result = VoiceResult.objects.create(voice=voice,
                                                  result_voice_file=f'Speech/release_files/convert_{name}_output.wav')
        voice_result.save()

        os.remove(wave_file)
        find_voice_result = VoiceResult.objects.get(voice=voice)
        for i in detection_info:
            voice_detail = VoiceDetail.objects.create(voice_result=find_voice_result,
                                                      detect_time=i['detect_time'],
                                                      command_detected=i['command_detected'])
            voice_detail.save()
    except Exception as exception:
        return f"error: {exception}"
