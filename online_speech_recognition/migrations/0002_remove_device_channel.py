# Generated by Django 4.2.4 on 2023-08-30 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_speech_recognition', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='channel',
        ),
    ]