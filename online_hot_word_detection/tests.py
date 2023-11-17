from django.test import TestCase
from psycopg2 import connect
from redis import Redis
from rest_framework.test import APIClient

from .models import Device


class VoiceModelTest(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_admin_panel(self):
        admin_panel = self.client.get('http://localhost:8000/admin/login/?next=/admin/')
        self.assertEqual(admin_panel.status_code, 200)

    def test_db_connection(self):
        connection = connect(
            "dbname='voice_recognition_db' user='voice_recognition_admin' host='localhost' "
            "password='SecurePas$14020529'")
        self.assertIsNotNone(connection)

    def test_message_broker_connection_offline(self):
        r = Redis(host="localhost", port=6379, db=1, socket_timeout=1)
        self.assertTrue(r.ping())

    def test_input_device_model(self):
        device = Device.objects.create(device_name="test", description="this is test")
        self.assertIsNotNone(device)

    def test_url_device_list(self):
        device_url = self.client.get('http://localhost:8000/online-voice/device-list/')
        self.assertEqual(device_url.status_code, 200)

    def test_url_device_list_method(self):
        device_url_1 = self.client.post('http://localhost:8000/online-voice/device-list/', data={"test": "test"})
        device_url_2 = self.client.put('http://localhost:8000/online-voice/device-list/', data={"test": "test"})
        device_url_3 = self.client.delete('http://localhost:8000/online-voice/device-list/', data={"test": "test"})
        self.assertNotEqual(device_url_1.status_code, 200)
        self.assertNotEqual(device_url_2.status_code, 200)
        self.assertNotEqual(device_url_3.status_code, 200)
