import os
import wave

import numpy as np
from celery import shared_task
from pydub import AudioSegment

from Speech.offline_stream_test import FrameASR

from .models import Voice, VoiceResult, VoiceDetail


@shared_task()
def offline_inference(wave_file, chime_file, out_dir, voice_id, step=0.25, window_size=2.0):
    try:
        """
        Arg:
            wav_file: wave file to be performed inference on.
            step: infer every step seconds
            window_size : length of audio to be sent to NN.
        """

        i = 0
        mbn_history = [0, 0, 0, 0]
        chimes = [wave_file]
        wave_name = os.path.split(wave_file)[-1]
        frame_len = step
        chunk_size = int(frame_len * 16000)

        mbn = FrameASR(model_definition={'densenet'}, frame_len=frame_len, frame_overlap=(window_size - frame_len) / 2,
                       offset=0)
        wf = wave.open(wave_file, 'rb')
        data = wf.readframes(chunk_size)
        detection_info = []
        while len(data) > 0:
            i += 1
            data = wf.readframes(chunk_size)
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
                audio_clip.export(f"{out_dir}/{wave_name[:-4]}_output.wav", format='wav')
                chimes.append(f"{out_dir}/{wave_name[:-4]}_output.wav")

        mbn.reset()
        split_text = wave_file.split('convert_')[-1]
        name = split_text.split('.')[0]
        voice = Voice.objects.get(id=voice_id)
        voice_result = VoiceResult.objects.create(voice=voice,
                                                  result_voice_file=f'Speech/release_files/convert_{name}_output.wav')
        voice_result.save()

        os.remove(wave_file)
        find_voice_result = VoiceResult.objects.get(voice=voice)
        for i in detection_info:
            voice_detail = VoiceDetail.objects.create(voice_result=find_voice_result,
                                                      detect_time=i['detect_time'],
                                                      command_detected=i['command_detected'])
            voice_detail.save()
    except Exception as error:
        return f"error: {error}"
