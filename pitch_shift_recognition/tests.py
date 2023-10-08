from os import path

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework.test import APIClient

from voice_manager.models import Voice
from .models import PitchShiftResult
from .pitch_shift.pitch_shift import Pitch_shift


class PitchShiftTest(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_create_pitch_shift_result(self):
        voice = None
        try:
            voice = Voice.objects.get(id=1)
            voice = PitchShiftResult.objects.create(sample_rate=42000, channel=4, file_extension='wav',
                                                    filename="../media/user_voices/1.wav", voice=voice)
            voice.save()
            self.assertIsNotNone(voice)
        except ValueError:
            self.assertIsNone(voice)
        except ObjectDoesNotExist:
            self.assertIsNone(voice)

    def test_read_pitch_shift_result(self):
        result = None
        try:
            result = PitchShiftResult.objects.get(pk=1)
            self.assertIsNotNone(result)
        except ObjectDoesNotExist:
            self.assertIsNone(result)

    def test_update_pitch_shift(self):
        result = None
        try:
            result = PitchShiftResult.objects.get(pk=1)
            result.sample_rate = 48000
            result.channel = 2
            result.file_extension = 'mp3'
            result.filename = '../media/user_voices/2.wav'
            self.assertIsNotNone(result)
        except ObjectDoesNotExist:
            self.assertIsNone(result)

    def test_delete_pitch_shift(self):
        result = None
        try:
            result = PitchShiftResult.objects.get(pk=1)
            result.delete()
        except ObjectDoesNotExist:
            self.assertIsNone(result)

    def test_pitch_shift_model(self):
        pitch_shift = Pitch_shift('pitch_shift_recognition/temp')
        test_file = 'media/user_voices/sp1.wav'
        name, file_path = pitch_shift.change_sr_ch(test_file)
        audio = pitch_shift.load(file_path)
        to_process, audio = pitch_shift.prepare(audio, 0, 0)
        board = pitch_shift.board_define(1)
        effected = pitch_shift.effect(board, to_process)
        output_dir = 'pitch_shift_recognition/output'
        output_file = pitch_shift.generate(audio, effected, name, output_dir, 1)
        pitch_shift.clean_temp(name)
        info = pitch_shift.get_log(output_file, 'wav')
        self.assertIsNotNone(info)
