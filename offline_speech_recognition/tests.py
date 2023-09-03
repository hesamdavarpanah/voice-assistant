from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from psycopg2 import connect
from redis import Redis
from rest_framework.test import APIClient

from .models import Voice


class VoiceModelTest(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_db_connection(self):
        connection = connect(
            "dbname='voice_recognition_db' user='voice_recognition_admin' host='localhost' "
            "password='SecurePas$14020529'")
        self.assertIsNotNone(connection)

    def test_message_broker_connection_offline(self):
        r = Redis(host="localhost", port=6379, db=0, socket_timeout=1)
        self.assertTrue(r.ping())

    def test_user_data(self):
        user = User.objects.filter(username='admin')
        self.assertIsNotNone(user)

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

    def test_admin_panel(self):
        admin_panel = self.client.get('http://localhost:8000/admin/login/?next=/admin/')
        self.assertEqual(admin_panel.status_code, 200)

    def test_crud_voice_url(self):
        crud_url = self.client.get("http://localhost:8000/offline-voice/crud-voice/")
        self.assertNotEqual(crud_url, 200)

    def test_offline_voice_detection_url(self):
        crud_url = self.client.get("http://localhost:8000/offline-voice/voice-detection/")
        self.assertNotEqual(crud_url, 200)
