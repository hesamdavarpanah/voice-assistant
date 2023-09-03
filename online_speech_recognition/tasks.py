import datetime

import numpy as np
import pyaudio as pa
import tensorflow as tf
from celery import shared_task

from Speech.online_stream_test import FrameASR
from online_speech_recognition.insert_redis_data import InsertData
from online_speech_recognition.redis_configer import RedisConfiguration


@shared_task()
def online(dev_idx, host, port, db_number, window_size=2.0, channels=1, rate=16000, frame_len=0.25):
    try:
        chunk_size = int(frame_len * rate)
        mbn_model = tf.keras.models.load_model('Speech/model.h5')
        mbn = FrameASR(mbn_model, frame_len=frame_len, frame_overlap=(window_size - frame_len) / 2, offset=0)
        mbn.reset()

        p = pa.PyAudio()

        mbn_history = [0, 0, 0, 0]

        stream = p.open(format=pa.paInt16,
                        channels=channels,
                        rate=16000,
                        input=True,
                        input_device_index=dev_idx,
                        frames_per_buffer=chunk_size)

        while True:
            data = stream.read(chunk_size)
            signal = np.frombuffer(data, dtype=np.int16)
            signal = signal.astype(np.float32) / 32768.
            mbn_result, data = mbn.transcribe(signal)
            mbn_history[:-1] = mbn_history[1:]
            if mbn_result == ['heyholoo']:
                mbn_history[-1] = 1
            else:
                mbn_history[-1] = 0

            if mbn_history[1:-1] == [0, 0] and mbn_history[-1] == 1:
                detect_time = datetime.datetime.now().strftime('%H:%M:%S')
                result = {'command': 'heyholoo'}
                redis_conf = RedisConfiguration(host, port, db_number)
                insert_data = InsertData(redis_conf.connection_pool, result, str(detect_time))
                insert_data.insert()
    except Exception as error:
        return f"error: {error}"
