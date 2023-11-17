from os import path, makedirs

from django.test import TestCase
from rest_framework.test import APIClient

from voice_manager.models import Voice
from voice_split.voice_splitter.high_denoise import Denoiser
from voice_split.voice_splitter.music_lownoise import Separator

from .models import HighDenoiseResult, LowDenoiseResult

from django.core.exceptions import ObjectDoesNotExist


class PitchShiftTest(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_create_voice_denoise_model(self):
        denoise = None
        try:
            voice = Voice.objects.get(id=1)
            denoise = DenoiseResult.objects.create(output_channels=2, output_sr=44100,
                                                            file_extension="wav",
                                                            output_file="voice_split/output_files/denoise_sp1.wav",
                                                            voice=voice)
            denoise.save()
            self.assertIsNotNone(denoise)
        except ObjectDoesNotExist:
            self.assertIsNone(denoise)

    def test_read_voice_denoise_model(self):
        denoise = DenoiseResult.objects.filter(id=1)
        self.assertIsNotNone(denoise)

    def test_update_voice_denoise_model(self):
        denoise = None
        try:
            denoise = DenoiseResult.objects.get(id=1)
            denoise.output_channels = 1
            denoise.output_sr = 1
            denoise.file_extension = 'wav'
            denoise.output_file = 'voice_split/output_files/denoise_sp1.wav'

            denoise.save()
            self.assertIsNotNone(denoise)
        except ObjectDoesNotExist:
            self.assertIsNone(denoise)

    def test_delete_high_voice_denoise_model(self):
        denoise = None
        try:
            denoise = DenoiseResult.objects.get(id=1)
            denoise.delete()
            self.assertIsNone(denoise)
        except ObjectDoesNotExist:
            self.assertIsNone(denoise)