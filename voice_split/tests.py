from os import path, makedirs

from django.test import TestCase
from rest_framework.test import APIClient

from voice_manager.models import Voice
from voice_split.voice_splitter.high_denoise import Denoiser
from voice_split.voice_splitter.music_lownoise import Separator

from .models import HighDenoiseResult, LowDenoiseResult

from django.core.exceptions import ObjectDoesNotExist


class PitchShiftTest(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_high_voice_denoise(self):
        test_file = 'media/user_voices/sp1.wav'
        high_voice_denoise = Denoiser('voice_split/temp')
        name, final_path = high_voice_denoise.change_sr(test_file)
        audio, sr = high_voice_denoise.load(final_path)
        audio = high_voice_denoise.convert(audio, sr)
        all_data = high_voice_denoise.denoise(audio, sr, name)
        output_files = "voice_split/output_files"
        output_file = high_voice_denoise.concat(all_data, name, output_files)
        high_voice_denoise.clean_temp(name, all_data)
        info = high_voice_denoise.get_log(output_file, 'wav')
        self.assertIsNotNone(info)

    def test_low_voice_denoise(self):
        test_file = 'media/user_voices/sp1.wav'
        basename = path.splitext(path.basename(test_file))[0]
        pretrained_model_path = "voice_split/voice_splitter/models/baseline.pth"

        sp = Separator(pretrained_model_path, 1024, 4, 256, 2048, -1)
        x_spec, sr = sp.spect(test_file, 44100)
        y_spec, v_spec = sp.separate(x_spec)
        output_files = "voice_split/output_files"

        if output_files != "":  # modifies output_dir if there is an arg specified
            output_files = output_files.rstrip('/') + '/'
            makedirs(output_files, exist_ok=True)

        vocal_file = '{}{}_Vocals.wav'.format(output_files, basename)
        sp.spec_to_wav(v_spec, vocal_file, sr)
        instrument_file = '{}{}_Instruments.wav'.format(output_files, basename)
        sp.spec_to_wav(y_spec, instrument_file, sr)

        if "wav" in ["ogg", "flac", "mp3", "aiff", "aac", "m4a"]:
            vocal_file = sp.change_format(vocal_file, "wav")
            instrument_file = sp.change_format(instrument_file, "wav")

        info = sp.get_log(vocal_file, instrument_file, sr, "wav")
        self.assertIsNotNone(info)

    def test_create_high_voice_denoise_model(self):
        high_denoise = None
        try:
            voice = Voice.objects.get(id=1)
            high_denoise = HighDenoiseResult.objects.create(output_channels=2, output_sr=44100,
                                                            file_extension="wav",
                                                            output_file="voice_split/output_files/denoise_sp1.wav",
                                                            voice=voice)
            high_denoise.save()
            self.assertIsNotNone(high_denoise)
        except ObjectDoesNotExist:
            self.assertIsNone(high_denoise)

    def test_read_high_voice_denoise_model(self):
        high_denoise = HighDenoiseResult.objects.filter(id=1)
        self.assertIsNotNone(high_denoise)

    def test_update_high_voice_denoise_model(self):
        high_denoise = None
        try:
            high_denoise = HighDenoiseResult.objects.get(id=1)
            high_denoise.output_channels = 1
            high_denoise.output_sr = 1
            high_denoise.file_extension = 'wav'
            high_denoise.output_file = 'voice_split/output_files/denoise_sp1.wav'

            high_denoise.save()
            self.assertIsNotNone(high_denoise)
        except ObjectDoesNotExist:
            self.assertIsNone(high_denoise)

    def test_delete_high_voice_denoise_model(self):
        high_denoise = None
        try:
            high_denoise = HighDenoiseResult.objects.get(id=1)
            high_denoise.delete()
            self.assertIsNone(high_denoise)
        except ObjectDoesNotExist:
            self.assertIsNone(high_denoise)
