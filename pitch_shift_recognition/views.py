from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import PitchShiftResultSerializers
from .models import PitchShiftResult
from os import path, mkdir
from voice_manager.models import Voice
from .pitch_shift.pitch_shift import Pitch_shift
from django.http import HttpResponse


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class PitchShiftProcessViewSet(ModelViewSet):
    queryset = PitchShiftResult.objects.all().order_by('publish_date')
    serializer_class = PitchShiftResultSerializers
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        output_files = 'pitch_shift_recognition/output_files'
        temp_dir = 'pitch_shift_recognition/temp'
        is_output_files = path.isdir(output_files)
        is_temp_dir = path.isdir(temp_dir)
        if not is_output_files:
            mkdir(output_files)
        if not is_temp_dir:
            mkdir(temp_dir)

        try:
            # user = User.objects.get(username=request.user.username)
            user = User.objects.get(id=1)
            voice = Voice.objects.get(id=request.data['voice_id'], user=user)
            pitch_shift = Pitch_shift(temp_dir)
            name, file_path = pitch_shift.change_sr_ch(voice.voice_file.path)
            audio = pitch_shift.load(file_path)
            to_process, audio = pitch_shift.prepare(audio, request.data['start'], request.data['end'])
            board = pitch_shift.board_define(request.data['step'])
            effected = pitch_shift.effect(board, to_process)
            output_file = pitch_shift.generate(audio, effected, name,
                                               output_files,
                                               request.data['step'])
            pitch_shift.clean_temp(name)
            if request.data['file_extension'] in ["ogg", "flac", "mp3", "aiff", "aac", "m4a"]:
                output_file = pitch_shift.change_format(output_file, request.data['file_extension'])
            info = pitch_shift.get_log(output_file, request.data['file_extension'])
            pitch_shift_result = PitchShiftResult.objects.create(sample_rate=info['output_sr'],
                                                                 channel=info['output_channels'],
                                                                 file_extension=info['output_format'],
                                                                 filename=info['output_file'],
                                                                 voice=voice)
            pitch_shift_result.save()
            message = "done"
            explanation = "the pitch shift voice is done"
            return Response({"message": message, "explanation": explanation}, status=200)
        except ObjectDoesNotExist:
            message = "not found"
            explanation = "the voice not found"

            return Response({"message": message, "explanation": explanation}, status=404)
        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)


class GetPitchShiftResultViewSet(ModelViewSet):
    queryset = PitchShiftResult.objects.all().order_by('publish_date')
    serializer_class = PitchShiftResultSerializers
    pagination_class = MyPagination
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        pitch_shift_result = PitchShiftResult.objects.all().order_by('publish_date')
        pitch_shift_result_serializer = PitchShiftResultSerializers(pitch_shift_result)
        return Response(data=pitch_shift_result_serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        pitch_shift_result_link = request.data["pitch_shift_result_link"]
        pitch_shift_result_file_extension = request.data["pitch_shift_result_file_extension"]
        f = open(pitch_shift_result_link, "rb")
        response = HttpResponse()
        response.write(f.read())
        response['Content-Type'] = f'audio/{pitch_shift_result_file_extension}'
        response['Content-Length'] = path.getsize(pitch_shift_result_link)
        return response
