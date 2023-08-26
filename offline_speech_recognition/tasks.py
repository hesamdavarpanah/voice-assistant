import os
import wave
from Speech.offline_stream_test import FrameASR
import numpy as np
from celery import shared_task
from pydub import AudioSegment


@shared_task()
def offline_inference(wave_file, chime_file, outdir, STEP=0.25, WINDOW_SIZE=2.0):
    """
    Arg:
        wav_file: wave file to be performed inference on.
        STEP: infer every STEP seconds
        WINDOW_SIZE : length of audio to be sent to NN.
    """

    i = 0
    mbn_history = [0, 0, 0, 0]
    chimes = [wave_file]
    wave_name = os.path.split(wave_file)[-1]
    FRAME_LEN = STEP
    CHANNELS = 1  # number of audio channels (expect mono signal)
    RATE = 16000  # sample rate, 16000 Hz
    CHUNK_SIZE = int(FRAME_LEN * 16000)

    mbn = FrameASR(model_definition={'densenet'}, frame_len=FRAME_LEN, frame_overlap=(WINDOW_SIZE - FRAME_LEN) / 2,
                   offset=0)
    wf = wave.open(wave_file, 'rb')
    data = wf.readframes(CHUNK_SIZE)
    detection_info = []
    while len(data) > 0:
        i += 1
        data = wf.readframes(CHUNK_SIZE)
        signal = np.frombuffer(data, dtype=np.int16)
        signal = signal.astype(np.float32) / 32768.
        mbn_result = mbn.transcribe(signal, j=i)
        mbn_history[:-1] = mbn_history[1:]
        if mbn_result[0] == ['heyholoo']:
            mbn_history[-1] = 1
        else:
            mbn_history[-1] = 0

        if mbn_history[1:-1] == [0, 0] and mbn_history[-1] == 1:
            pos = (i - 1) * 4000 / 16000
            detection_info.append({'command_detected': 'heyholoo', 'detect_time': pos})

            audio_clip = AudioSegment.from_wav(chimes[-1])
            chime = AudioSegment.from_wav(chime_file)
            audio_clip = audio_clip.overlay(chime, position=pos * 1000)
            audio_clip.export(f"{outdir}/{wave_name[:-4]}_output.wav", format='wav')
            chimes.append(f"{outdir}/{wave_name[:-4]}_output.wav")

    mbn.reset()
    return detection_info
