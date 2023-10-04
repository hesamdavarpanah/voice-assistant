from django.contrib.auth.models import User
from django.test import TestCase
from psycopg2 import connect
from redis import Redis
from rest_framework.test import APIClient


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

    def test_admin_panel(self):
        admin_panel = self.client.get('http://localhost:8000/admin/login/?next=/admin/')
        self.assertEqual(admin_panel.status_code, 200)

    def test_crud_voice_url(self):
        crud_url = self.client.get("http://localhost:8000/offline-voice/crud-voice/")
        self.assertNotEqual(crud_url, 200)

    def test_offline_voice_detection_url(self):
        crud_url = self.client.get("http://localhost:8000/offline-voice/voice-detection/")
        self.assertNotEqual(crud_url, 200)
