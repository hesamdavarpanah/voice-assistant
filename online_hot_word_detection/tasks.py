import datetime
import numpy as np
import pyaudio as pa
import tensorflow as tf
from celery import shared_task

from online_hot_word_detection.insert_redis_data import InsertData
from online_hot_word_detection.redis_configer import RedisConfiguration


@shared_task()
def online(host, port, db_number, window_size=2.0, channels=1, rate=16000, frame_len=0.25):
    try:
        """
            put your hot word detection algorithm here
        """
        detect_time = datetime.datetime.now().strftime('%H:%M:%S')
        result = {'command': 'your_command'}
        redis_conf = RedisConfiguration(host, port, db_number)
        insert_data = InsertData(redis_conf.connection_pool, result, str(detect_time))
        insert_data.insert()
    except Exception as exception:
        return f"error: {exception}"
