from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from .models import Voice


class VoiceModelTest(TestCase):
    def test_create_voice_data(self):
        voice = None
        try:
            user = User.objects.filter(username="random")
            voice = Voice.objects.create(title="test", description="this is test",
                                         voice_file="media/user_voices/sp1_1todVkB.wav", user=user)
            self.assertIsNotNone(voice)
        except ValueError:
            self.assertIsNone(voice)

    def test_read_voice_data(self):
        voice = None
        try:
            voice = Voice.objects.get(pk=1)
            self.assertIsNotNone(voice)
        except ObjectDoesNotExist:
            self.assertIsNone(voice)

    def test_update_voice_data(self):
        voice = None
        try:
            voice = Voice.objects.get(pk=1)
            voice.title = "tested"
            voice.save()
            self.assertIsNotNone(voice)
        except ObjectDoesNotExist:
            self.assertIsNone(voice)

    def test_delete_voice_data(self):
        voice = None
        try:
            voice = Voice.objects.get(pk=1)
            voice.delete()
            voice = Voice.objects.filter(pk=1)
            self.assertIsNotNone(voice)
        except ObjectDoesNotExist:
            self.assertIsNone(voice)
