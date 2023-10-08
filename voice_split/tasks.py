from os import path, mkdir, makedirs

from celery import shared_task
from django.contrib.auth.models import User

from voice_manager.models import Voice
from voice_split.voice_splitter.high_denoise import Denoiser
from .models import HighDenoiseResult, LowDenoiseResult
from .voice_splitter.music_lownoise import Separator


@shared_task()
def high_denoise_task(voice_id, file_extension, temp_dir, output_files):
    # user = User.objects.get(username=request.user.username)
    user = User.objects.get(id=1)
    voice = Voice.objects.get(id=voice_id, user=user)
    high_voice_denoise = Denoiser(temp_dir)
    name, final_path = high_voice_denoise.change_sr(voice.voice_file.path)
    audio, sr = high_voice_denoise.load(final_path)
    audio = high_voice_denoise.convert(audio, sr)
    all_data = high_voice_denoise.denoise(audio, sr, name)
    output_file = high_voice_denoise.concat(all_data, name, output_files)
    high_voice_denoise.clean_temp(name, all_data)
    info = high_voice_denoise.get_log(output_file, file_extension)
    high_denoise = HighDenoiseResult.objects.create(output_file=info['output_file'],
                                                    output_sr=info['output_sr'],
                                                    output_channels=info['output_channels'],
                                                    file_extension=file_extension,
                                                    voice=voice)
    high_denoise.save()


@shared_task()
def low_denoise_task(voice_id, hop_length, batch_size, crop_size, n_fft, sr, file_extension):
    user = User.objects.get(id=1)
    voice = Voice.objects.get(id=voice_id, user=user)
    basename = path.splitext(path.basename(voice.voice_file.path))[0]
    pretrained_model_path = "voice_split/voice_splitter/models/baseline.pth"

    sp = Separator(pretrained_model_path, hop_length,
                   batch_size, crop_size, n_fft, -1)
    x_spec, sr = sp.spect(voice.voice_file.path, sr)
    y_spec, v_spec = sp.separate(x_spec)
    output_files = "voice_split/output_files"

    if output_files != "":  # modifies output_dir if there is an arg specified
        output_files = output_files.rstrip('/') + '/'
        makedirs(output_files, exist_ok=True)

    vocal_file = '{}{}_Vocals.wav'.format(output_files, basename)
    sp.spec_to_wav(v_spec, vocal_file, sr)
    instrument_file = '{}{}_Instruments.wav'.format(output_files, basename)
    sp.spec_to_wav(y_spec, instrument_file, sr)

    if file_extension in ["ogg", "flac", "mp3", "aiff", "aac", "m4a"]:
        vocal_file = sp.change_format(vocal_file, file_extension)
        instrument_file = sp.change_format(instrument_file, file_extension)

    info = sp.get_log(vocal_file, instrument_file, sr, file_extension)
    low_denoise_result = LowDenoiseResult.objects.create(vocal_file=info['vocal_file'],
                                                         instrument_file=info['instrument_file'],
                                                         output_sr=info['output_sr'],
                                                         output_channels=info['output_channels'],
                                                         file_extension=file_extension,
                                                         voice=voice)
    low_denoise_result.save()
